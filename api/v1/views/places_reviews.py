#!/usr/bin/python3
""" place reviews API module """
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all States
    """
    list_ = []
    all_states = storage.all(State)
    if state_id:
        state = all_states.get("State." + state_id, None)
        return state.to_dict() if state else abort(404)
    else:
        for value in all_states.values():
            list_.append(value.to_dict())
        return jsonify(list_), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def save_state():
    """Creates a State
    """
    body = request.get_json()
    if request.is_json:
        if "name" in body.keys():
            state = State(**body)
            state.save()
            return jsonify(state.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error='Not a JSON'), 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """Updates a Amenity object
    """
    body = request.get_json()
    all_states = storage.all(State)
    state = all_states.get("State." + state_id, None)
    if state is None:
        abort(404)
    elif not request.is_json:
        return jsonify(error='Not a JSON'), 400

    for m, n in body.items():
        if m in ['id', 'updated_at', 'updated_at']:
            continue
        setattr(state, m, n)
    state.save()
    return jsonify(state.to_dict()), 200
