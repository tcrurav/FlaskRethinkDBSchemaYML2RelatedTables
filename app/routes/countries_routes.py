# app/countries/routes.py
from flask import Blueprint, request, jsonify
from app.controllers.countries_controller import create_country, get_countries, get_country, get_array_of_bicycles_by_country_id, update_country, delete_country

main = Blueprint('Countries', __name__)

@main.route('/api/countries', methods=['GET'])
def list_countries():
    countries = get_countries()
    return jsonify(countries), 200

@main.route('/api/countries/<string:country_id>', methods=['GET'])
def get_single_country(country_id):
    country = get_country(country_id)
    if country:
        return jsonify(country), 200
    return jsonify({"error": "Country not found"}), 404

@main.route('/api/countries/<string:country_id>/bicycles', methods=['GET'])
def get_array_of_bicycles_by_country(country_id):
    bicycles = get_array_of_bicycles_by_country_id(country_id)
    if bicycles:
        return jsonify(bicycles), 200
    return jsonify({"error": "Country not found"}), 404

@main.route('/api/countries', methods=['POST'])
def create_new_country():
    data = request.json
    create_country(data)
    return jsonify({"message": "Country created"}), 201

@main.route('/api/countries/<string:country_id>', methods=['PUT'])
def update_existing_country(country_id):
    data = request.json
    update_country(country_id, data)
    return jsonify({"message": "Country updated"}), 200

@main.route('/api/countries/<string:country_id>', methods=['DELETE'])
def delete_existing_country(country_id):
    delete_country(country_id)
    return jsonify({"message": "Country deleted"}), 200