from flask import Flask
from flask import json

# g object provided by flask is used for 
# storing common data during requests or cli commands.
# g stands for "global".
from flask import g

from flask import request

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

# Create Read Update Delete (CRUD)

# create one = POST
@app.route('/item', methods=['POST'])
def create_item():
    name = request.form['name']
    value = request.form['value']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO items (name, value) VALUES (?,?)', (name, value))
    conn.commit()

    return app.response_class(
        response = json.dumps([{'action':'Added new item'}, {'new item': cur.lastrowid}]),
        status = 200,
        mimetype = 'application/json'
    )

# read all = GET
@app.route('/items')
def get_items():
    data = []

    cur = get_db().cursor()
    cur.execute('SELECT id, name, value FROM items')

    rows = cur.fetchall()
    for row in rows:
        data.append({'id': row[0], 'name': row[1], 'value': row[2]})

    return app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

# read one = GET
@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM items WHERE id = ?', (id,))

    item = cur.fetchone()
    return app.response_class(
        response = json.dumps([{'action':'testing'}, item]),
        status = 200,
        mimetype = 'application/json'
    )

# update one = PUT
@app.route('/item', methods=['PUT'])
def update_item():
    conn = get_db()
    cur = conn.cursor()

    id = request.form['id']
    value = request.form['value']

    cur.execute('UPDATE items SET value = ? WHERE id = ?', (value, id))
    conn.commit()

    return app.response_class(
        response = json.dumps([{'action': 'Updated item'}, {'id': id}]),
        status = 200,
        mimetype='application/json'
    )


# delete one = DELETE
@app.route('/item', methods=['DELETE'])
def delete_item():
    id = request.form['id']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE id = ?',(id,))
    conn.commit()

    return app.response_class(
        response = json.dumps([{'action': 'Deleted item'}, {'id':id}]),
        status = 200,
        mimetype = 'application/json'
    )
