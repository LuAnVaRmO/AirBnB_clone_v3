#!/usr/bin/python3
""" States API module """
from . import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id=None):
    """ get all reviews by place request """
    list_rev = []
    all_places = storage.get(Place, place_id)
    if all_places:
        rev = place.reviews
        for value in rev:
            list_.append(value.to_dict())
        return jsonify(list_rev), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id=None):
    """ get review by ID """
    rev = storage.get(Review, review_id)
    return rev.to_dict() if rev else abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """ send review """
    body = request.get_json()

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400
    if "user_id" not in body.keys():
        return jsonify(error="Missing user_id"), 400

    user = storage.get(User, body["user_id"])
    if not user:
        abort(404)
    if "text" not in body.keys():
        return jsonify(error="Missing text"), 400
    rev = Review(place_id=place_id, **body)
    rev.save()
    return jsonify(rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """ Update review """
    review = storage.get(Review, review_id)
    body_dic = request.get_json()
    if not review:
        abort(404)
    elif not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in body_dic.items():
        if key in ['id', 'user_id', 'place_id', 'updated_at', 'updated_at',
                   'state_id']:
            continue
        setattr(review, key, value)
    review.save()


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ Delete review by id """
    rev = storage.get(Review, review_id)
    if rev:
        storage.delete(rev)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
