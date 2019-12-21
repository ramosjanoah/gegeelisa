from model import *
from service.wikipedia_scrape_service import WikipediaScrapeService
from .serializer import WikipediaNodeSerializer
from .base import Base
from helper import *

class ExpandNode(Base):
	def __init__(self, node, show_internal_reference=3):
		self.node = node
		self.show_internal_reference = show_internal_reference


	def perform(self):
		self.validate()
		result = self.expand_node()
		return result


	def validate(self):
		if self.node is None:
			raise NodeNotFound
		if self.node.page().state != PageStateEnum(0):
			raise PageHasBeenExpanded
		return


	def expand_node(self):
		scrape_result = WikipediaScrapeService.scrape_founded_page(self.node.string_id)

		total_adjacents = 0
		for ref in scrape_result.internal_reference:
			checked_node = WikipediaNode.find_by_string_id(ref.string_id)
			if checked_node is None:
				referenced_node = WikipediaNode(ref.id, ref.string_id)
			else:
				referenced_node = checked_node
			self.node.referenced_to.add(referenced_node)
			referenced_node.save()
			total_adjacents += 1
		self.node.save_reference()

		self.set_cached_internal_references(self.node)

		serializer = WikipediaNodeSerializer(node=self.node, show_internal_reference=self.show_internal_reference)
		serializer.total_adjacents = total_adjacents

		return serializer
