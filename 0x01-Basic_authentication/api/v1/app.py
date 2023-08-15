#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth_type = os.getenv("AUTH_TYPE", "auth")

if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.errorhandler(401)
def unauthorized(error):
    """
    Function to handle unautorize access
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Function to handle error 403
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """
    Method to handle the request filtering and validation
    """
    if auth is None:
        return

    allowed_paths = ['/api/v1/status/', 'api/v1/unauthorized/', 'api/v1/forbidden/']
    if request.path not in allowed_paths and not auth.require_auth(request.path, allowed_paths):
        abort(401) if auth.authorization_headers(request) is None else abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
