if __name__ == '__main__':
    exit(1)

URLDB = None

def getUrldb(db):
    global URLDB
    if URLDB != None:
        return URLDB
    class Urldb(db.Model):
        __tablename__ = 'urldb'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.Text, nullable=False)
        orgn_url = db.Column(db.Text, nullable=False, unique=True)
        shrt_url = db.Column(db.Text, nullable=False, unique=True)
        def __init__(self, username, original, shortened):
            self.username = username
            self.orgn_url = original
            self.shrt_url = shortened
        def __repr__(self):
            return '%s::%s' % (
                self.orgn_url,
                self.shrt_url
            )
        def get_original_url(self):
            return self.orgn_url
    URLDB = Urldb
    return URLDB
