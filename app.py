from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from dbconfig import dbconfig
from dbmodels.urldb import getUrldb
from dbmodels.userdb import getUserdb

app = Flask(__name__)
db = dbconfig(app)

Urldb = getUrldb(db)
Userdb = getUserdb(db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth'


@login_manager.user_loader
def user_loader(username):
    return Userdb.query.filter_by(username=username).first()


@app.route('/')
@login_required
def index():
    return redirect('/home', code=302)


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    pass


@app.route('/home')
@login_required
def home():
    pass


@app.route('/history')
@login_required
def history():
    pass


@app.route('/r/<url>')
def external_redirect(url):
    original = Urldb.query().filter_by(shrt_url=url).first().get_original_url()
    return redirect(original, code=307)


if __name__ == '__main__':
    app.run(debug=True)
