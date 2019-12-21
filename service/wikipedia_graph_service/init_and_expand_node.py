from model import *
from service.wikipedia_scrape_service import WikipediaScrapeService
from .serializer import WikipediaNodeSerializer
from .base import Base
from helper import *

class InitAndExpandNode(Base):
	def __init__(self, string_id, show_internal_reference=3):
		self.string_id = string_id
		self.show_internal_reference = show_internal_reference


	def perform(self):
		self.validate()
		result = self.init_and_expand_node()
		return result


	def validate(self):
		# raise if Node has been build
		if WikipediaNode.find_by_string_id(self.string_id) is not None:
			raise NodeHasBeenBuild
		return


	def init_and_expand_node(self):
		scrape_result = WikipediaScrapeService.scrape_unfounded_page(self.string_id)

		new_node = WikipediaNode(scrape_result.page.id, scrape_result.page.string_id)
		new_node.save()

		total_adjacents = 0
		for ref in scrape_result.internal_reference:
			checked_node = WikipediaNode.find_by_string_id(ref.string_id)
			if checked_node is None:
				referenced_node = WikipediaNode(ref.id, ref.string_id)
			else:
				referenced_node = checked_node
			new_node.referenced_to.add(referenced_node)
			referenced_node.save()
			total_adjacents += 1
		new_node.save_reference()

		self.set_cached_internal_references(new_node)
		serializer = WikipediaNodeSerializer(node=new_node, show_internal_reference=self.show_internal_reference)
		serializer.total_adjacents = total_adjacents

		return serializer
