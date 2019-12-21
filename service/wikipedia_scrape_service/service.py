from urllib.request import urlopen
from functools import lru_cache

import repository
from repository import redis
from repository import beautiful_soup

from model import WikipediaPage, WikipediaPageComponent, PageStateEnum

from .scrape_unfounded_page import ScrapeUnfoundedPage
from .scrape_founded_page import ScrapeFoundedPage

from helper import *

class WikipediaScrapeService():
	def __init__(self):
		pass

	def scrape_unfounded_page(self, page_id, **kwargs):
		return ScrapeUnfoundedPage(page_id, kwargs).perform()

	def scrape_founded_page(self, page_id, **kwargs):
		return ScrapeFoundedPage(page_id, kwargs).perform()



if __name__ == '__main__':
	pass
else:
	WikipediaScrapeService = WikipediaScrapeService()
