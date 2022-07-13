#encoding: utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from main import app
# from models import User,Boss,Recruit

manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()