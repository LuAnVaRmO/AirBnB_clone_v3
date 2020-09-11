#!/usr/bin/python3
""" Places API module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_place(city_id=None):
    """ get all places or place by city id request """

    list_ = []
    city = storage.get(City, city_id)
    if city:
        places = city.places
        for place in places:
            list_.append(place.to_dict())
        return jsonify(list_), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """ get all places or place by id request """
    place = storage.get(Place, place_id)
    if place:
        return place.to_dict()

    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id=None):
    """ create a place """

    body = request.get_json()
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if "user_id" not in body.keys():
        return jsonify(error="Missing user_id"), 400

    user = storage.get(User, body['user_id'])

    if user is None:
        abort(404)

    if "name" not in body.keys():
        return jsonify(error="Missing name"), 400
    place = Place(city_id=city_id, **body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """ Update a place """
    body = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'user_id', 'city_id']:
            continue
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
