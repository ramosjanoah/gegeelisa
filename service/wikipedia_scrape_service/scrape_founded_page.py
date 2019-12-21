from model import WikipediaPage, WikipediaPageComponent, PageStateEnum
from .base import Base
from .serializer import WikipediaScrapeSerializer
from helper import *

class ScrapeFoundedPage(Base):
	def __init__(self, string_id, kwargs):
		super().__init__()
		self.string_id = string_id
		self.page = WikipediaPage.get_by_string_id(string_id)
		self.save = kwargs.get('save', True)
		self.scrape_from = kwargs.get('scrape_from', None)
		self.check_first = kwargs.get('save', True)
		self.output = None
		self.components = []


	def perform(self):
		self.validate()
		result = self.scrape_founded_page()
		return result


	def scrape_founded_page(self):
		self.page.scrapped_from = self.scrape_from
		self.output = WikipediaScrapeSerializer()
		self.output.page = self.page
		if self.save_page_component: self.components = self.get_wikipedia_components(self.string_id)
		self.output.internal_reference = self.get_wikipedia_internal_reference(self.string_id)
		if self.save: self.save_all()

		return self.output


	def validate(self):
		if self.check_first:
			if self.page is None:
				raise PageNotFound
			if self.page.state == PageStateEnum(1):
				raise PageHasBeenScrapped
			return

		if self.save: # if doesn't check but saved, then error
			raise PageSavedButNotChecked
		return


	def save_all(self):
		if self.output is None or self.output.page is None:
			raise PageHasNotBeenSet

		self.output.page.add()

		for c in self.components:
			c.add()

		for i, reference in enumerate(self.output.internal_reference):
			check = WikipediaPage.get_by_string_id(reference.string_id)
			if check is not None:
				self.output.internal_reference[i] = check
			else:
				reference.add()

		if self.save_page_component:
			self.output.page.change_state_to_scrapped()
		else:
			self.output.page.change_state_to_expanded()
