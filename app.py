from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from config.dbconfig import dbconfig
from dbmodels.urldb import getUrldb
from dbmodels.userdb import getUserdb

app = Flask(__name__)
db = dbconfig(app)

Urldb = getUrldb(db)
Userdb = getUserdb(db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth'


def create_response(info_username = None, info_password = None, info_confpassword = None, info_title = None, info_msg = None, content = None):
    res = {}
    res['info'] = {}
    res['info']['username'] = info_username
    res['info']['password'] = info_password
    res['info']['confpassword'] = info_confpassword
    res['info']['title'] = info_title
    res['info']['msg'] = info_msg
    res['content'] = content
    return res


@login_manager.user_loader
def user_loader(username):
    return Userdb.query.filter_by(username=username).first()


@app.route('/')
@login_required
def index():
    return redirect('/home', code=302)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET': return render_template('register.html',
        form = {
            'username': '',
            'password': '',
            'confpassword': ''
        },
        res = create_response()
    )
    username = request.form.get('username')
    password = request.form.get('password')
    confpassword = request.form.get('confpassword')
    username = username.strip()
    if len(username) < 5 or len(username) > 9: render_template('register.html',
        form = {
            'username': username,
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_username = True,
            info_title = 'username must have 5 to 9 characters',
            info_msg = 'username must have 5 to 9 characters'
        )
    )
    if chars := is_invalid(username): render_template('register.html',
        form = {
            'username': username,
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_username = True,
            info_title = 'invalid username',
            info_msg = 'username cannot contain any of ' + chars
        )
    )
    if password != confpassword: render_template('register.html',
        form = {
            'username': username,
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_password = True,
            info_title = 'passwords didn\'t match',
            info_msg = 'passwords didn\'t match'
        )
    )
    if len(password) < 8: render_template('register.html',
        form = {
            'username': username,
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_password = True,
            info_title = 'password should exceed 8 characters',
            info_msg = 'password should exceed 8 characters'
        )
    )
    if missing := is_missing_char(password): render_template('register.html',
        form = {
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_password = True,
            info_title = 'password should contain ' + missing,
            info_msg = 'password should contain ' + missing
        )
    )
    try:
        u = Userdb(username, password)
    except e as Exception: render_template('error.html',
        form = {
            'username': username,
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_title = 'Registration Error',
            info_msg = 'Details:\n' + e
        )
    )
    return redirect('/auth', code=302)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    return render_template('auth.html',
        form = {
            'username': '',
            'password': '',
            'confpassword': ''
        },
        res = create_response()
    )


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
