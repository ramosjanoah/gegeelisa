from helper import *

class WikipediaNodeSerializer():
	def __init__(self, node=None, show_internal_reference=3, total_adjacents=None):
		self.node = node
		self.show_internal_reference = show_internal_reference
		self.total_adjacents = total_adjacents

	def serialize(self, http_status=200):
		if self.node is None:
			raise NodeNotFound

		result = {}
		result['data'] = {
			'node': self.serialize_node(self.node),
			'internal_adjacents': self.serialize_internal_adjacents()
		}

		meta = {}
		if self.total_adjacents: meta['total_adjacents'] = self.total_adjacents
		meta['http_status'] = http_status
		result['meta'] = meta
	
		return result

	def serialize_internal_adjacents(self):
		result = []
		for rnode in self.node.referenced_to:
			result.append(self.serialize_node(rnode))
			if len(result) == self.show_internal_reference:
				break
		return result

	def serialize_node(self, node):
		words = node.string_id.split('_')
		initial = ""

		for word in words:
			if word[0] != "(":
				initial += word[0].upper()
			if len(initial) >= 3:
				break
		
		url = 'https://en.wikipedia.org/wiki/{}'.format(node.string_id)

		return {
			'page_id': node.page_id,
			'string_id': node.string_id,
			'initial': initial,
			'url': url,
		}

class WikipediaAdjacentsSerializer(WikipediaNodeSerializer):
	def __init__(self, internal_adjacents=[], total_adjacents=None):
		self.internal_adjacents = internal_adjacents
		self.total_adjacents = total_adjacents

	def serialize(self, http_status=200):

		result = {}
		result['data'] = {
			'internal_adjacents': self.serialize_internal_adjacents()
		}

		meta = {}
		if self.total_adjacents: meta['total_adjacents'] = self.total_adjacents
		meta['http_status'] = http_status
		result['meta'] = meta
	
		return result

	def serialize_internal_adjacents(self):
		result = []
		for rnode in self.internal_adjacents:
			result.append(self.serialize_node(rnode))
		return result
