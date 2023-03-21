from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == '__main__':
    exit(1)

USERDB = None

def getUserdb(db):
    global USERDB
    if USERDB != None:
        return USERDB
    class Userdb(db.Model):
        __tablename__ = 'userdb'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(9), nullable=False, unique=True)
        passhash = db.Column(db.String(128), nullable=False)
        def __init__(username, password):
            if len(username) < 5: raise Error('username too short')
            if len(username) > 9: raise Error('username too long')
            if len(password) < 8: raise Error('password too short')
            self.username = username
            self.passhash = generate_password_hash(password)
        def __repr__():
            return '%d:%s' % (
                self.id,
                self.username
            )
        def authenticate(password):
            return check_password_hash(self.passhash, password)
    USERDB = Userdb
    return USERDB
