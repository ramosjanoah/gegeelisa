from urllib.request import urlopen
import repository
from repository import beautiful_soup

from model import *
from helper import *
from env import env

class Base():
	wikipedia_url = 'https://en.wikipedia.org/wiki/'
	internal_identifier = '/wiki/'
	max_internal_reference = 12
	max_page_components = 6

	def __init__(self):
		self.save_page_component = env['SAVE_PAGE_COMPONENT']

	def get_wikipedia_components(self, page_id):
		"""
			return: WikipediaComponentsPage from Wikipedia Page with id = page_id
		"""

		scrapped_components = self.scrape_wikipedia_components(page_id)
		components = []

		for component in scrapped_components:
			if component['text'] == '':
				continue
			component_objects = WikipediaPageComponent(
					page_id=page_id,
					content_type=component['type'],
					content=replace_newline(component['text']))

			components.append(component_objects)
		return components


	def scrape_wikipedia_components(self, page_id, limit=max_page_components):
		"""
			return: array of dictionary with field: 'text', 'type', the base of WikipediaPageComponent
		"""
		soup = self.scrape_wikipedia_soup(page_id)
		body = soup.find('div', {'id': 'content'})

		components = body.findAll(['h1', 'h2', 'p'])

		result = []
		for i, component in enumerate(components):
			if i == limit:
				break
			component_hash = {
				'text': component.text,
				'type': component.name
			}
			result.append(component_hash)
		return result


	def get_wikipedia_internal_reference(self, page_id):
		"""
			return: WikipediaPage which appear in WikipediaPage with id = page_id
		"""

		scrapped_internal_reference = self.scrape_wikipedia_reference_internal(page_id)
		internal_reference = []

		for reference in scrapped_internal_reference:
			if reference['string_id'] is None:
				continue
			r = WikipediaPage(string_id=reference['string_id'])
			r.title = reference['title']
			r.state = PageStateEnum(0)

			internal_reference.append(r)

		return internal_reference


	def scrape_wikipedia_reference_internal(self, page_id, limit=max_internal_reference):
		"""
			return: array of dictionary with field: 'text', 'type', the base of WikipediaPageComponent
		"""

		sett = set([])
		soup = self.scrape_wikipedia_soup(page_id)
		body = soup.find('div', {'id': 'content'})
		all_href = body.findAll('a')
		internal_reference = []
		for i, href in enumerate(all_href):
			if len(sett) == limit:
				break
			if not href.attrs.get('href', False) or not href.attrs.get('title', False):
				continue
			if ':' in href.attrs['href']:
				continue
			if href.attrs['href'][0:6] != self.internal_identifier:
				continue
			if href.attrs['href'][6:] in sett:
				continue
			internal_reference.append({
					'title': href.attrs['title'],
					'string_id': href.attrs['href'][6:],
			})
			sett.add(href.attrs['href'][6:])

		return internal_reference

	def scrape_wikipedia_soup(self, page_id):
		try:
			url = self.wikipedia_url + page_id

			page = urlopen(url)
			content = page.read()
			soup = beautiful_soup(content, 'html.parser')
			return soup
		except Exception as e:
			raise ScrapePageError
	
