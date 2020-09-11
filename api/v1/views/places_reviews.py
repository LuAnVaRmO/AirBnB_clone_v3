#!/usr/bin/python3
""" States API module """
from api.v1.views import app_views
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.review import Review
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id=None):
    """ get all reviews by place request """
    list_ = []
    all_places = storage.all(Place)
    if place_id:
        places = all_places.get("Place." + place_id, None)
        return places.to_dict() if state else abort(404)
    else:
        for value in all_places.values():
            list_.append(value.to_dict())
        return jsonify(list_), 200


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id=None):
    """ get review by ID """
    review = storage.get(Review, review_id)
    return review.to_dict() if review else abort(404)


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
    review = Review(place_id=place_id, **body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """ Update review """
    review = storage.get(Review, review_id)
    if review:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            if key in ['id', 'user_id', 'place_id', 'updated_at', 'updated_at',
                       'state_id']:
                continue
            setattr(state, key, value)
        review.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
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
