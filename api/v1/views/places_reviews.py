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
    list_rev = []
    all_places = storage.get(Place, place_id)
    if all_places:
        rev = place.reviews
        for value in rev:
            list_.append(value.to_dict())
        return jsonify(list_rev), 200
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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, kwargs["user_id"])
    if user is None:
        abort(404)
    if "text" not in kwargs:
        return jsonify({"error": "Missing text"}), 400
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
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
