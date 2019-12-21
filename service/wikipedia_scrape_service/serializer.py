# serializer

class WikipediaScrapeSerializer:
	def __init__(self, page=None, components=None, internal_references=None):
		self.page = page
		self.components = components
		self.internal_reference = internal_references