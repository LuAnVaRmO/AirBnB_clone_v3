#!/usr/bin/python3
""" User API module """

from models.user import User
from . import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """ get all users or user by id request """

    list_ = []
    all_users = storage.all(User)
    if user_id:
        user = all_users.get("User." + user_id, None)
        return user.to_dict() if user else abort(404)
    else:
        for value in all_users.values():
            list_.append(value.to_dict())
        return jsonify(list_), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Create user """

    body = request.get_json()
    if request.is_json:
        if "email" not in body.keys():
            return jsonify(error="Missing email"), 400
        elif "password" not in body.keys():
            return jsonify(error="Missing password"), 400
        else:
            user = User(**body)
            user.save()
            return jsonify(user.to_dict()), 201
    return jsonify(error='Not a JSON'), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """ Update user """

    body = request.get_json()
    all_users = storage.all(User)
    user = all_users.get("User." + user_id, None)
    if user is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for k, v in body.items():
        if k in ['id', 'updated_at', 'updated_at', 'email']:
            continue
        setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """ Delete a user """

    all_users = storage.all(User)
    user = all_users.get("User." + user_id, None)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
