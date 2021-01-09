from flask import Flask
from flask import json

# g object provided by flask is used for 
# storing common data during requests or cli commands.
# g stands for "global".
from flask import g

import sqlite3

DATABASE = 'sample.db'

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

def teardown_db(execption):
    db = g.pop('db')
    if db is not None:
        db.close()

@app.route('/')
def deploy():
    return 'Hello world!'

@app.route('/items')
def get_items():
    data = []

    cur = get_db().cursor()
    cur.execute('SELECT name, value FROM items')

    rows = cur.fetchall()
    for row in rows:
        data.append({'name':row[0], 'value':row[1]})

    return app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
