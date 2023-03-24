# URL Shortener

To make a URL Shortener webapp using Python and Flask.

### Run
```
pip install -r requirements.txt
python setup.py
python app.py
```

### The Directory Structure
```
root/
├── config/
│   ├── dbconfig.py
│   └── envars.py
├── data/
│   └── data.sqlite3
├── dbmodels/
│   ├── userdb.py
│   ├── urldb.py
│   ├── schema_userdb.sql
│   └── schema_urldb.sql
├── docs/
│   └── userdb.py
├── templates/
│   ├── auth.html
│   ├── error.html
│   ├── history.html
│   ├── home.html
│   ├── layout.html
│   └── register.html
├── app.py
├── requirements.txt
├── setup.py
└── README.md
```

#### app.py
The app entry point. The app can be started by the following command
```
python setup.py
python app.py
```

**environment variables:**

`APP_HOSTNAME`: This is the hostname where the app is hosted.
For localhost, it may look something like `localhost:5000`.
For online hosting it may look something like `urlshortener.hosting.app`.

#### setup.py
This file needs to be executed prior to the app.
If not, the app will quit and ask the user to run `setup.py`.

This file initizes the database file in `data/data.sqlite3`.

The module uses `sqlite3` to programmatically create the database and the tables `urldb` and `userdb`.

The conventional procedure
```
flask db init
flask db migrate
```

did not work, perhaps because a `Termux` environment was used as a more conventional development environment was unavailable.

However, this method is functional and has no apparent comprises.

Setup script will simply quit if the database already exists.

#### config/
It holds the configuration for the database and a module to load environment variables.

`dbconfig.py` configures `SQLALCHEMY_DATABASE_URI` and others.

#### data/
Contains one and only `data.sqlite3` which is the database file.

This file is gitignored, and needs to be created by running the setup script.

#### dbmodels/
Perhaps one of the most important part of the app.

The python modules hold classes which serve as the models for the tables `urldb` and `userdb`.

These classes are returned by functions to the `__main__` module.

`userdb` stores authentication information. `urldb` stores original and short url information.

The SQL schema files are loaded by `setup.py` to create `data/data.sqlite3`.

### Workflow
- A user visits `/`.
- `/` requires login, if user may get redirected to `/auth`.
- `/` itself redirects user to `/home`.
- `/auth` requires user to authenticate themselves.
- Alternately, the user can click on `Sign up` to register.
- Username length is limited to 5 to 8 characters.
- Password length should be atleast 8 characters.
- Errors are displayed if user already exists, or if constraints are not satisfied.
- Once registered, user is redirected to `/auth`.
- Once authenticated, user is redirected to `/home`.
- This is where the user enters a URL and on submit, gets the shortened URL.
- The shortening algorithm uses the first 7 characters of the `SHA-256` hash of the (original URL concatenated with the username).
- These 7 characters form a `key` which is used as a variable path (i.e. endpoint).
- Assume the 7 characters end up being `92d9a9`.
- Then the shortened URL is `<domain>/r/92d9a9`.
- If domain is `localhost:5000` then the URL is `localhost:5000/r/92d9a9`
- The home page links to the history page, which is a table of list of all URLs shortened by a user.

A thing of note is that if the original URL already exists in the database for a user, it's short URL is reused from there and is not recreated for the current user.

### Challenges faced
Creating a proper template structure that's easy to debug was challenging.
Using a single layout file made the structure complicated.

Secondly, flask couldn't be used to intialise the database.
The challenge was figuring out the fact that `sqlite3` module can be used to intialise the database.

Thirdly, building a proper project structure, and taking care of which module should call whom.

Finally, the structure of the data that was to be sent to the templates had to be decided.
This was the most challenging part of the project as care had to be taken that `NoneType` wasn't sent to certain parts of the template but also it had to be made sure that certain parts of the template didn't get activated.

Quite a few edge cases were taken care of.

### Things learned
This project was a great learning experience. It was challenging, and had certain complexities.

There are a few points that were noted when building this project:

- db init isn't the only was to intialise a flask database.
- flask makes authentication very easy; there was no need to handle cookies.
- commiting to a database may cause integrity error. one is supposed to rollback the database in such a case.
- so try-except blocks were used to handle such scenarios
