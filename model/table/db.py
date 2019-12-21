from flask_sqlalchemy import SQLAlchemy
from gegeelisa import gegeelisa

db = SQLAlchemy()
db.init_app(gegeelisa)
