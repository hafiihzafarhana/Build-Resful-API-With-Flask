## Activate Virtual Environment

Command (CMD / Bash):

- `py -3 -m venv .venv`
- `source .venv\Scripts\activate`
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
- `Werkzeug`

### After install python-dotenv: pip install python-dotenv

- `python-dotenv`
