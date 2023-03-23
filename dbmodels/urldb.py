if __name__ == '__main__':
    exit(1)

from sqlalchemy import exc

URLDB = None

def getUrldb(db):
    global URLDB
    if URLDB != None:
        return URLDB
    class Urldb(db.Model):
        __tablename__ = 'urldb'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.Text, nullable=False)
        original_url = db.Column(db.Text, nullable=False)
        short_key = db.Column(db.Text, nullable=False, unique=True)
        def __init__(self, username, original, shortened):
            self.username = username
            self.original_url = original
            self.short_key = shortened
            db.session.add(self)
            try:
                db.session.commit()
            except (exc.IntegrityError, Exception) as e:
                if isinstance(e, exc.IntegrityError):
                    db.session.rollback()
                else: raise Exception(str(e))
        def __repr__(self):
            return '%s::%s' % (
                self.original_url,
                self.short_key
            )
        def get_original_url(self):
            return self.original_url
    return (URLDB := Urldb)
