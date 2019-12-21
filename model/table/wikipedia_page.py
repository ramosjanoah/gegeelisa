from .db import db
import enum
from datetime import datetime
from helper import *

class PageStateEnum(enum.Enum):
    found = 0
    expanded = 1
    scrapped = 2

# We didn't pass app instance here.
class WikipediaPage(db.Model):
    __tablename__ = 'wikipedia_pages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    string_id = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255), nullable=False)
    found_at = db.Column(db.DateTime(), default=datetime.utcnow)
    scrapped_from = db.Column(db.String(255), default=None)
    scrapped_at = db.Column(db.DateTime(), default=None)
    state = db.Column(db.Enum(PageStateEnum))

    def __init__(self, **kwargs):
        self.string_id = kwargs.get('string_id', None)
        if self.string_id is None:
            raise Exception('string_id must be filled. Input: {}'.format(self.string_id))

        self.title = kwargs.get('title', self.string_id)
        self.scrapped_from = kwargs.get('scrapped_from', None)
        self.scrapped_at = kwargs.get('scrapped_at', None)
        self.state = PageStateEnum(kwargs.get('state', (0)))

    def add(self, skip_error=True):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if skip_error:
                print(e)
                print(type(e))
            else:
                raise e

    def update(self, skip_error=True):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if skip_error:
                print(e)
                print(type(e))
            else:
                raise e


    def change_state_to_expanded(self):
        self.state = PageStateEnum(1)
        self.scrapped_at = datetime.utcnow()
        self.update()


    def change_state_to_scrapped(self):
        self.state = PageStateEnum(2)
        self.scrapped_at = datetime.utcnow()
        self.update()

    @classmethod
    def get_by_string_id(cls, string_id):
        return cls.query.filter_by(string_id=string_id).first()

    def node(self, string_id):
        node = WikipediaNode.find_by_string_id(self.string_id)
        if node is None:
            raise NodeNotFound
        return node
