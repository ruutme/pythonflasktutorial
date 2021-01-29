from flask import Flask
from flask import json

# g object provided by flask is used for 
# storing common data during requests or cli commands.
# g stands for "global".
from flask import g

from flask import request

import sqlite3

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, scoped_session

from models import Item

DATABASE = 'sample.db'

app = Flask(__name__)
engine = create_engine('sqlite:///' +  DATABASE)

# Create base class that stores all classes representing the tables
Base = declarative_base()
Base.metadata.reflect(bind=engine)

# Create configured session class
Session_factory = sessionmaker(bind=engine)
session = scoped_session(Session_factory)

# Create all tables that don't exist yet
Base.metadata.create_all(engine)

@app.teardown_request
def remove_session(ex=None):
    session.remove()

@app.route('/')
def deploy():
    return 'Hello world!'

# Create Read Update Delete (CRUD)

# create one = POST
@app.route('/item', methods=['POST'])
def create_item():
    name = request.form['name']
    value = request.form['value']
    
    new_item = Item(name=name, value=value)
    session.add(new_item)
    session.commit()

    return app.response_class(
        response = json.dumps([{'action':'Added new item'}, {'new item': new_item.id}]),
        status = 200,
        mimetype = 'application/json'
    )

# read all = GET
@app.route('/items')
def get_items():
    data = []
    
    rows = session.query(Item).all()

    for row in rows:
        data.append({'id': row.id, 'name': row.name, 'value': row.value})

    return app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

# read one = GET
@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):

    item = session.query(Item).filter(Item.id == id).first()
    
    return app.response_class(
        response = json.dumps([{'action':'testing'}, {'id': item.id, 'name': item.name, 'value': item.value}]),
        status = 200,
        mimetype = 'application/json'
    )

# update one = PUT
@app.route('/item', methods=['PUT'])
def update_item():
    id = request.form['id']
    value = request.form['value']

    session.query(Item).filter(Item.id == id).update({'value': value}, synchronize_session='fetch')
    session.commit()

    return app.response_class(
        response = json.dumps([{'action': 'Updated item'}, {'id': id}]),
        status = 200,
        mimetype='application/json'
    )

# delete one = DELETE
@app.route('/item', methods=['DELETE'])
def delete_item():
    id = request.form['id']

    session.query(Item).filter(Item.id == id).delete()
    session.commit()

    return app.response_class(
        response = json.dumps([{'action': 'Deleted item'}, {'id':id}]),
        status = 200,
        mimetype = 'application/json'
    )
