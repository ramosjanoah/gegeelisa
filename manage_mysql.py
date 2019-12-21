from model import *
from model.table.db import db
from gegeelisa import gegeelisa
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

db.init_app(gegeelisa)
migrate = Migrate(gegeelisa, db)
manager = Manager(gegeelisa)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
