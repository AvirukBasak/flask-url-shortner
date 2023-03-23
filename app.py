from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from config.dbconfig import dbconfig
from dbmodels.urldb import getUrldb
from dbmodels.userdb import getUserdb

import hashlib

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


def shorten_url(original):
    hash = hashlib.sha256((original + current_user.username).encode("UTF-8")).hexdigest()
    return hash[:7]


def create_response(
    info_username = None,
    info_password = None,
    info_confpassword = None,
    info_link = None,
    info_shortkey = None,
    info_title = None,
    info_msg = None,
    content = None,
    info_error = False
):
    res = {}
    res['info'] = {}
    res['info']['error'] = info_error
    res['info']['username'] = info_username
    res['info']['password'] = info_password
    res['info']['confpassword'] = info_confpassword
    res['info']['link'] = info_link
    res['info']['shortkey'] = info_shortkey
    res['info']['title'] = info_title
    res['info']['msg'] = info_msg
    res['content'] = content
    return res


def err_auth_response(username, password, confpassword, template, error_at, title, msg = None, code = 400):
    if not msg: msg = title
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
def user_loader(u):
    return db.session.get(Userdb, u)


@app.route('/')
@login_required
def index():
    return redirect('/home', code=302)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_active: return redirect('/home', code=302)
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
    if len(username) < 5 or len(username) > 9: return err_auth_response(
        username, password, confpassword, 'register.html', 'username',
        title = 'username must have 5 to 9 characters'
    )
    if chars := is_username_invalid(username): return err_auth_response(
        username, password, confpassword, 'register.html', 'username',
        title = 'invalid username',
        msg = 'username cannot contain any of ' + chars
    )
    if password != confpassword: return err_auth_response(
        username, password, confpassword, 'register.html', 'confpassword',
        title = 'passwords didn\'t match'
    )
    if len(password) < 8: return err_auth_response(
        username, password, confpassword, 'register.html', 'password',
        title = 'password should exceed 8 characters'
    )
    if missing := is_missing_char(password): return err_auth_response(
        username, password, confpassword, 'register.html', 'password',
        title = 'password should contain ' + missing
    )
    try:
        u = Userdb.query.filter_by(username=username).first()
        if u: return err_auth_response(
            username, password, confpassword, 'register.html', 'username',
            title = 'an account with this username already exists'
        )
        u = Userdb(username, password)
        if not u.id: raise Exception('registration failed')
    except Exception as e: return err_auth_response(
        username, password, confpassword, 'error.html', 'error',
        title = 'Registration Error',
        msg = str(e),
        code = 500
    )
    return redirect('/auth', code=302)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_active: return redirect('/home', code=302)
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
    if len(username) < 5 or len(username) > 9 or is_username_invalid(username): return err_auth_response(
        username, password, None, 'auth.html', 'username',
        title = 'invalid username'
    )
    try:
        u = Userdb.query.filter_by(username=username).first()
        flag = u.authenticate(password) if u else False
        if not flag: return err_auth_response(
            username, password, None, 'auth.html', 'password',
            title = 'invalid username or password'
        )
        login_user(u)
    except Exception as e: return err_auth_response(
        username, password, None, 'error.html', 'error',
        title = 'Authentication Error',
        msg = str(e),
        code = 500
    )
    next = request.args.get('next')
    if next: redirect(next, code=302)
    return redirect('/', code=302)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET': return render_template('home.html',
        form = { 'link': '' },
        res = create_response()
    )
    link = request.form.get('link')
    link = link.strip()
    if not link: return render_template('home.html',
        form = { 'link': link },
        res = create_response(
            info_link = True,
            info_msg = 'invalid url'
        )
    ), 400
    shortkey = shorten_url(link)
    username = current_user.username
    try:
        url = Urldb.query.filter_by(original_url=link).first()
        if url: url = Urldb(username, link, url.short_key)
        if url: return render_template('home.html',
            form = { 'link': link },
            res = create_response(
                info_shortkey = '<a href="/r/%s">https://localhost:5000/r/%s</a>' % (
                    url.short_key,
                    url.short_key
                )
            )
        )
        url = Urldb(username, link, shortkey)
        if not url.id: raise Exception('server error')
    except Exception as e: return render_template('error.html',
            form = { 'link': link },
            res = create_response(
                info_error = True,
                info_title = 'Server Error',
                info_msg = str(e)
            )
        ), 500
    return render_template('home.html',
        form = { 'link': link },
        res = create_response(
            info_shortkey = '<a href="/r/%s" target="_blank">https://localhost:5000/r/%s</a>' % (
                shortkey,
                shortkey
            )
        )
    )


@app.route('/history')
@login_required
def history():
    def ret_split(el): 
        (url, key) = str(el).rsplit('::', 1)
        return (url, key)
    content = Urldb.query.filter_by(username=current_user.username)
    content = list(map(ret_split, content))
    print(content)
    return render_template('history.html',
        form = {},
        res = create_response(content=content)
    )


@app.route('/r/<key>')
def external_redirect(key):
    original = Urldb.query.filter_by(short_key=key).first()
    if not original: return render_template('error.html',
        form = {},
        res = create_response(
            info_error = True,
            info_title = 'Not Found',
            info_msg = 'The given URL was not found'
        )
    ), 404
    original = original.get_original_url()
    return redirect(original, code=307)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)
