from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from model import WikipediaPage
from repository import graph
from helper import *
import enum

class WikipediaNode(GraphObject):
	__primarykey__ = 'page_id'

	page_id = Property()
	string_id = Property()
	state = Property()
	title = Property()

	referenced_to = RelatedTo('WikipediaNode')

	def __init__(self, page_id, string_id, state=0, title=None):
		self.page_id = page_id
		self.string_id = string_id
		if title is None:
			self.title = string_id
		self.state = state

	@classmethod
	def find_by_string_id(cls, string_id):
		return cls.match(graph).where("_.string_id = '{}'".format(string_id)).first()

	@classmethod
	def find_by_page_id(cls, page_id):
		return cls.match(graph, page_id).first()

	def save(self):
		graph.push(self)

	def add_reference(self, wikipedia_node):
		self.referenced_to.add(wikipedia_node)

	def save_reference(self):
		graph.push(self.referenced_to)

	def save_all(self):
		self.save()
		self.save_reference()

	def page(self):
		page = WikipediaPage.get_by_string_id(self.string_id)
		if page is None:
			raise PageNotFound
		return page
