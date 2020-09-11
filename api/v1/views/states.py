#!/usr/bin/python3
""" States API module """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """ get all states or state by id request """
    list_ = []
    all_states = storage.all(State)
    if state_id:
        state = all_states.get("State." + state_id, None)
        return state.to_dict() if state else abort(404)
    else:
        for value in all_states.values():
            list_.append(value.to_dict())
        return jsonify(list_), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ send state """
    body = request.get_json()
    if "name" not in body:
        return jsonify({'error': 'Missing name'}), 400
    if not body:
        return jsonify({'error': 'Not a JSON'}), 400
    new_state = State(**body)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Update state """
    state = storage.get(State, state_id)
    if state:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'created_at']
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete state """
    state_ = storage.get(State, state_id)
    if state_:
        storage.delete(state_)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
