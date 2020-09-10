#!flask/bin/python
""" RestFul API """
from models import storage
from os import getenv
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Close the session """
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        h = getenv('HBNB_API_HOST')
    else:
        h = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        p = getenv('HBNB_API_PORT')
    else:
        p = 5000
    app.run(host=h,port=p)
    threaded = True
