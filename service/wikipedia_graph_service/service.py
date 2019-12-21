from urllib.request import urlopen
from functools import lru_cache
import re

from repository import graph
from service.wikipedia_scrape_service import WikipediaScrapeService

from model import WikipediaNode, WikipediaPage

from helper import *

from .serializer import WikipediaNodeSerializer, WikipediaAdjacentsSerializer
from .init_and_expand_node import InitAndExpandNode
from .expand_node import ExpandNode
from .retrieve_adjacent_nodes import RetrieveAdjacentNodes
from .base import Base

class WikipediaGraphService(Base):
	"""
		docstring for WikipediaGraphService
	"""
	def __init__(self):
		pass

	def retrieve_node_by_page_id(self, page_id):
		node = WikipediaNode.find_by_page_id(page_id)
		return WikipediaNodeSerializer(node=node)


	def retrieve_node_by_string_id(self, string_id):
		node = WikipediaNode.find_by_string_id(string_id)
		return WikipediaNodeSerializer(node=node)

	def init_and_expand_node(self, string_id, show_internal_reference=3):
		return InitAndExpandNode(string_id, show_internal_reference).perform()

	def expand_node_by_string_id(self, string_id):
		node = WikipediaNode.find_by_string_id(string_id)
		if node is None:
			raise NodeNotFound
		return self.expand_node(node)

	def expand_node(self, node, show_internal_reference=3):
		if not isinstance(node, WikipediaNode):
			raise InvalidType('node', WikipediaNode)
		return ExpandNode(node).perform()

	def retrieve_adjacent_nodes_by_string_id(self, string_id, offset=0, limit=3):
		cache, total = self.get_cached_internal_references(string_id, offset, limit)
		if cache is not None:
			return WikipediaAdjacentsSerializer(cache, total)

		node = WikipediaNode.find_by_string_id(string_id)
		if node is None:
			raise NodeNotFound

		result = self.retrieve_adjacent_nodes(node, offset, limit)
		return result
		

	def retrieve_adjacent_nodes(self, node, offset=0, limit=3):
		if not isinstance(node, WikipediaNode):
			raise InvalidType('node', WikipediaNode)
		return RetrieveAdjacentNodes(node, offset, limit).perform()


	def get_random_node(self, page_id, amount=3):
		raise NotImplementedError


if __name__ == '__main__':
	pass
else:
	WikipediaGraphService = WikipediaGraphService()
