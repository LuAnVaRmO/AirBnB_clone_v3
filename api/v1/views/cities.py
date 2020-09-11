#!/usr/bin/python3
""" Cities API module """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city(state_id=None):
    """ Get all cities or cities by state """
    list_ = []
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        list_ = []
        for value in cities:
            list_.append(value.to_dict())
        return jsonify(list_), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id=None):
    """ Get all cities or cities by state """

    city = storage.get(City, city_id)
    if city:
        return city.to_dict()
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Update City """
    city = storage.get(City, city_id)
    if city:
        body = request.get_json()
        if not body:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body.items():
            ignore_keys = ['id', 'state_id', 'created_at']
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Create City """
    body = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not body:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in body:
        return jsonify({'error': 'Missing name'}), 400

    new_city = City(**body)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete city """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
