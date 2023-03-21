from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

if __name__ == '__main__':
    exit(1)

def dbconfig(app):
    cwd = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + os.path.join(cwd, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
    Migrate(app, db)
    return db
