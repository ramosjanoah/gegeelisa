from flask import Flask
from env import env, db_uri

gegeelisa = Flask(__name__,
			template_folder='view/templates',
			static_folder='view/static')

gegeelisa.config['SQLALCHEMY_DATABASE_URI'] = db_uri
gegeelisa.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
gegeelisa.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

gegeelisa.debug = env['DEBUG_MODE']
