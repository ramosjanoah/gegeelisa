# wikipedia page service
from model import *

class WikipediaPageService():
    def __init__(self):
        pass

    def get(self, page_id):
        return WikipediaPage.query.filter_by(string_id=page_id).first()

if __name__ == '__main__':
	pass
else:
    WikipediaPageService = WikipediaPageService()
