if __name__ == '__main__':
    exit(1)

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == '__main__':
    exit(1)

USERDB = None

def getUserdb(db):
    global USERDB
    if USERDB != None:
        return USERDB
    class Userdb(db.Model, UserMixin):
        __tablename__ = 'userdb'
        id = db.Column(db.Integer, nullable=False, primary_key=True)
        username = db.Column(db.String(9), nullable=False, unique=True)
        passhash = db.Column(db.String(128), nullable=False)
        def __init__(self, username, password):
            if len(username) < 5: raise Error('username too short')
            if len(username) > 9: raise Error('username too long')
            if len(password) < 8: raise Error('password too short')
            self.username = username
            self.passhash = generate_password_hash(password)
            try:
                db.session.add(self)
                db.session.commit()
            except Exception as e:
                raise Exception(str(e))
        def __repr__(self):
            return '%s:%s' % (
                self.id,
                self.username
            )
        def authenticate(self, password):
            return check_password_hash(self.passhash, password)
    return (USERDB := Userdb)
