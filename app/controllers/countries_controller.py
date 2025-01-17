# app/controllers/countries_controller.py
from rethinkdb import RethinkDB
from flask import current_app, jsonify
import yaml
from cerberus import Validator

r = RethinkDB()

RETHINKDB_HOST = current_app.config["RETHINKDB_HOST"]
RETHINKDB_PORT = current_app.config["RETHINKDB_PORT"]
RETHINKDB_DB   = current_app.config["RETHINKDB_DB"]

# Load schema from app/schemas/country_schema.yml
with open('app/schemas/country_schema.yml', 'r') as file:
    schema = yaml.safe_load(file)
    country_schema = schema['country_schema']

# Cerberus Validator initialized with the loaded schema
v = Validator(country_schema)

def create_country(data):
    """ Insert a new country into the 'countries' table """
    # Validate using schema
    if not v.validate(data):
        return jsonify({'error': 'Invalid data', 'details': v.errors}), 400
    
    with r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB) as conn:
        return r.table('countries').insert(data).run(conn)

def get_countries():
    """ Retrieve all countries from the 'countries' table """
    with r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB) as conn:
        return list(r.table('countries').run(conn))
    
def get_array_of_bicycles_by_country_id(country_id):
    """ Retrieve the bicycles field from of country_id in the 'countries' table """
    with r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB) as conn:
        return list(r.table('countries').filter({'id': country_id}).pluck('bicycles').run(conn))

def get_country(country_id):
    """ Retrieve a single country by ID """
    with r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB) as conn:
        return r.table('countries').get(country_id).run(conn)

def update_country(country_id, data):
    """ Update a country by ID """
    # Validate using schema
    if not v.validate(data):
        return jsonify({'error': 'Invalid data', 'details': v.errors}), 400
    
    with r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB) as conn:
        return r.table('countries').get(country_id).update(data).run(conn)

def delete_country(country_id):
    """ Delete a country by ID """
    with r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB) as conn:
        return r.table('countries').get(country_id).delete().run(conn)