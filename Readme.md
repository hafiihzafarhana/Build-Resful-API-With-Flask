## Activate Virtual Environment

Command (CMD / Bash):

- `py -3 -m venv .venv`
- `source .venv/Scripts/activate`
- `which python` (For know where environment i am using for, is local or global? use local)

## Deactivate Virtual Environment

Command (CMD / Bash):

- `deactivate`

## How to start or running?

- `flask --app testing run --host=0.0.0.0 --debug`

## How to running in development?

### (by default running in production)

- bash: `export FLASK_ENV=development`
- CMD: `set FLASK_ENV=development`

## What variable was set before?

`export FLASK_ENV=development`
`export FLASK_APP=flaskr`

## Folder Structure
- .venv
- flaskr/
    - config
    - constant
    - controllers
    - database
    - repositories
    - routes
    - services
    - static
    - templates
    - utils
    - __init__.py
- tests/
    - 
- .env
- .flaskenv
- instance/
    - file.db

## How to generate table of database?
- go to command and write `flask shell`
- `from flaskr.database.database import db`
- `db.create_all()`
- `db` and the result is `<SQLAlchemy sqlite:///D:\dev2\Cryce Truly\rest_api_py_flask\instance\bookmark.db>`

## What package installed?

### After install flask: pip install Flask

- `MarkupSafe`
- `itsdangerous`
- `colorama`
- `blinker`
- `Werkzeug`
- `Jinja2`
- `click`
- `flask`

### After install watchdog: pip install Watchdog

- `watchdog`

### After install python-dotenv: pip install python-dotenv

- `python-dotenv`

### After install SQLAlchemy: pip install SQLAlchemy

- `SQLAlchemy`

### After install Flask-SQLAlchemy: pip install Flask-SQLAlchemy
