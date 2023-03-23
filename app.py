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


def is_missing_char(password):
    return None


def is_username_invalid(username):
    return None


def create_response(info_username = None, info_password = None, info_confpassword = None, info_title = None, info_msg = None, content = None, info_error = False):
    res = {}
    res['info'] = {}
    res['info']['error'] = info_error
    res['info']['username'] = info_username
    res['info']['password'] = info_password
    res['info']['confpassword'] = info_confpassword
    res['info']['title'] = info_title
    res['info']['msg'] = info_msg
    res['content'] = content
    return res


def create_err_response(username, password, confpassword, template, error_at, title, msg, code = 400):
    if error_at not in ['username','password','confpassword','error']:
        raise Exception('\'%s\' is not a valid input name' % error_at)
    return render_template(
        template,
        form = {
            'username': username,
            'password': password,
            'confpassword': confpassword
        },
        res = create_response(
            info_username = error_at == 'username',
            info_password = error_at == 'password',
            info_confpassword = error_at == 'confpassword',
            info_error = error_at == 'error',
            info_title = title,
            info_msg = msg
        )
    ), code


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
    if len(username) < 5 or len(username) > 9: return create_err_response(
        username, password, confpassword, 'register.html', 'username',
        title = 'username must have 5 to 9 characters',
        msg = 'username must have 5 to 9 characters'
    )
    if chars := is_username_invalid(username): return create_err_response(
        username, password, confpassword, 'register.html', 'username',
        title = 'invalid username',
        msg = 'username cannot contain any of ' + chars
    )
    if password != confpassword: return create_err_response(
        username, password, confpassword, 'register.html', 'confpassword',
        title = 'passwords didn\'t match',
        msg = 'passwords didn\'t match'
    )
    if len(password) < 8: return create_err_response(
        username, password, confpassword, 'register.html', 'password',
        title = 'password should exceed 8 characters',
        msg = 'password should exceed 8 characters'
    )
    if missing := is_missing_char(password): return create_err_response(
        username, password, confpassword, 'register.html', 'password',
        title = 'password should contain ' + missing,
        msg = 'password should contain ' + missing
    )
    try:
        u = Userdb(username, password)
        if not u.id: raise Exception('registration failed')
    except Exception as e: return create_err_response(
        username, password, confpassword, 'error.html', 'error',
        title = 'Registration Error',
        msg = str(e),
        code = 500
    )
    return redirect('/auth', code=302)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET': return render_template('auth.html',
        form = {
            'username': '',
            'password': ''
        },
        res = create_response()
    )
    username = request.form.get('username')
    password = request.form.get('password')
    username = username.strip()
    if len(username) < 5 or len(username) > 9 or is_username_invalid(username): return create_err_response(
        username, password, None, 'auth.html', 'username',
        title = 'invalid username',
        msg = 'invalid username'
    )
    try:
        u = Userdb.query.filter_by(username=username).first()
        flag = u.authenticate(password) if u else False
        if not flag: return create_err_response(
            username, password, None, 'auth.html', 'password',
            title = 'invalid username or password',
            msg = 'invalid username or password'
        )
    except Exception as e: return create_err_response(
        username, password, None, 'error.html', 'error',
        title = 'Authentication Error',
        msg = str(e),
        code = 500
    )
    return redirect('/home', code=302)


@app.route('/home')
@login_required
def home():
    return render_template('home.html',
        form = {
            'link': ''
        },
        res = create_response()
    )


@app.route('/history')
@login_required
def history():
    return render_template('history.html',
        form = {},
        res = create_response()
    )


@app.route('/r/<key>')
def external_redirect(key):
    original = Urldb.query.filter_by(short_key=key).first().get_original_url()
    return redirect(original, code=307)


if __name__ == '__main__':
    app.run(debug=True)
