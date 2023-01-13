import sqlite3
import click
from flask import current_app, g

def get_db():
    # g is a unique object for each request, that is used to store data accessed by multiple functions
    if 'db' not in g:
        # sqlite3.connect establishes a connection to the file pointed at by DATABASE config key
        g.db = sqlite3.connect(
            # current_app is a object that points to the Flask app handling the request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells the connection to return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # returns a database connection
    db = get_db()

    # open resource opens a file relative to flaskr
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
# shows a success message to the user.
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)