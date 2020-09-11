#!/usr/bin/python3
""" Amenities API module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """ get all amenities or amenity by id request """

    list_ = []
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict()), 200
        abort(404)
    else:
        amenities = storage.all(Amenity)
        for amenity in amenities.values():
            list_.append(amenity.to_dict())
        return jsonify(list_), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ Delete amenity """

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates a Amenity """

    body = request.get_json()
    if request.is_json:
        if "name" in body.keys():
            amenity = Amenity(**body)
            amenity.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error='Not a JSON'), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """ Update a Amenity """

    body = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at']:
            continue
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
