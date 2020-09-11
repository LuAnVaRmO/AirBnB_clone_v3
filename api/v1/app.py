#!/usr/bin/python3
""" RestFul API """
from models import storage
from os import getenv
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Close the session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Display error message """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default='5000'),
        threaded=True
    )
