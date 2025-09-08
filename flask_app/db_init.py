import sqlite3, click
from datetime import datetime
from flask import g, current_app


#Connects to the sqlite database
def db_connect():
    #g is unique for every request and stores data
    if 'db' not in g:
        g.db = sqlite3.connect(
            #current points to app that handles request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #Row tells connection to return rows
        g.db.row_factory = sqlite3.Row
    return g.db


#If connection exists, it is closed
def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


#Initialises the database and also open the SQL file
def init_db():
    db = db_connect()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

#Initialises app by closing database connection and adding the init-db command
def init_app(app):
    #Calls this when cleaning up after response has been returned
    app.teardown_appcontext(close_db_connection)
    #Adds new cmd that can be called with flask
    app.cli.add_command(init_db_cmd)


#Click is for quick setup via a custom command line command
@click.command('init-db')
def init_db_cmd():
    init_db()
    click.echo('Database init SUCCESS')

#Converts timestamp type items into datetime(i think)
sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)


