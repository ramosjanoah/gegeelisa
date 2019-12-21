from model import WikipediaPage, WikipediaPageComponent, PageStateEnum
from .base import Base
from .serializer import WikipediaScrapeSerializer
from helper import *

class ScrapeUnfoundedPage(Base):
	def __init__(self, page_id, kwargs):
		super().__init__()
		self.page_id = page_id
		self.save = kwargs.get('save', True)
		self.scrape_from = kwargs.get('scrape_from', None)
		self.check_first = kwargs.get('save', True)
		self.output = None
		self.components = []


	def perform(self):
		self.validate()
		result = self.scrape_unfounded_page()
		return result


	def scrape_unfounded_page(self):
		"""
			params kwargs:
			- save: save page to database
			- referer: referer page when scrape this page (TODO)
			- skip_if_done: skip all the operation already on database (TODO)
			return:
			- WikipediaScrapeSerializer Object with all filled
		"""

		page = WikipediaPage(
			string_id=self.page_id,
			title=self.page_id,
			scrapped_from=self.scrape_from)

		page.scrapped_from = self.scrape_from
		self.output = WikipediaScrapeSerializer()
		self.output.page = page
		if self.save_page_component: self.components = self.get_wikipedia_components(self.page_id)
		self.output.internal_reference = self.get_wikipedia_internal_reference(self.page_id)

		if self.save: self.save_all()

		return self.output


	def validate(self):
		if self.check_first:
			w = WikipediaPage.get_by_string_id(self.page_id)
			if w is not None:
				if w.state == PageStateEnum(1):
					raise PageHasBeenScrapped					
				elif w.state == PageStateEnum(0):
					raise PageHasBeenFounded
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
