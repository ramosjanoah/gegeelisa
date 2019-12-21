from model import *
from service.wikipedia_scrape_service import WikipediaScrapeService
from .serializer import WikipediaAdjacentsSerializer
from .base import Base
from helper import *

class RetrieveAdjacentNodes(Base):
	def __init__(self, node, offset, limit):
		self.node = node
		self.offset = offset
		self.limit = limit


	def perform(self):
		self.validate()
		adjacents = self.retrieve_adjacent_nodes()
		adjacents.sort(key=lambda x: x.page_id)

		self.set_cached_internal_references(self.node)

		total_adjacents = len(adjacents)
		adjacents = adjacents[self.offset:self.offset+self.limit]
		result = WikipediaAdjacentsSerializer(internal_adjacents=adjacents, total_adjacents=total_adjacents)
		return result


	def validate(self):
		if self.node is None:
			raise NodeNotFound
		return


	def retrieve_adjacent_nodes(self):
		referenced_node = self.node.referenced_to
		adjacents = []
		for node in referenced_node:
			adjacents.append(node)

		return adjacents
