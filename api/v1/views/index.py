#!/usr/bin/python3
""" Index page """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def route():
    """ Return a Json response """
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
