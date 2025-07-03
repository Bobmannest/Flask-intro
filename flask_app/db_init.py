import sqlite3

from flask import g, current_app


#Connects to the sqlite database
def db_connect():
    #g is unique for every request and stores data
    if 'db' not in g:
        g.db = sqlite3.connect(
            #current points to app that handles request
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        #Row tells connection to return rows
        g.db.row_factory = sqlite3.Row
    return g.db

#If connection exists, it is closed
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
