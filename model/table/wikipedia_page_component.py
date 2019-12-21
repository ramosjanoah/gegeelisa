from .db import db
from datetime import datetime
import string

# We didn't pass app instance here.
class WikipediaPageComponent(db.Model):
    __tablename__ = 'wikipedia_page_components'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.String(255), index=True, nullable=False)
    content_type = db.Column(db.String(255), default=None)
    content = db.Column(db.UnicodeText, default=None)
    scrapped_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.page_id = kwargs.get('page_id', None)
        if self.page_id is None:
            raise Exception('page_id must be filled')

        self.content_type = kwargs.get('content_type', None)
        self.content = kwargs.get('content', None)
        if len(self.content) > 0:
            self.content = ''.join(x for x in self.content if x in string.printable)
        self.scrapped_at = kwargs.get('scrapped_at', None)

    def add(self, skip_error=True):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if skip_error:
                print(e)
            else:
                raise e
