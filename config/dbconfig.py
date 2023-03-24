if __name__ == '__main__':
    exit(1)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets
import os

import envars

if __name__ == '__main__':
    exit(1)

if not os.path.isfile('data/data.sqlite3'):
    print('database doesn\'t exist')
    print('run setup.py')
    exit(1)

def dbconfig(app):
    datapath = os.path.abspath(
        os.path.join(
            os.path.join(
                os.path.join(
                    os.path.dirname(__file__), '..'), 'data'), 'data.sqlite3'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + datapath
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secrets.token_hex()
    db = SQLAlchemy(app)
    Migrate(app, db)
    return db
