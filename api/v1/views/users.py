#!/usr/bin/python3
""" module for users query """

from api.v1.views import app_views
from flask import jsonify, abort, request
import models


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Returns all the users"""
    all_user = models.storage.all("User")
    new_dict = [val.to_dict() for val in all_user.values()]
    return jsonify(new_dict)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates user"""
    json = request.get_json()
    User = models.user.User
    if json is not None:
        if json.get("email") is not None:
            if json.get("password") is not None:
                obj = User(email=json.get("email"),
                           password=json.get("password"))
                obj.save()
                return jsonify(obj.to_dict()), 201
            else:
                abort(400, "Missing password")
        else:
            abort(400, "Missing email")
    else:
        abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def userId(user_id):
    """Returns the user with an id"""
    obj = models.storage.get("User", user_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def user_del(user_id):
    """ return empty dict with 200 status"""
    obj = models.storage.get("User", user_id)
    if obj is not None:
        models.storage.delete(obj)
        models.storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Returns the user with an id"""
    obj = models.storage.get("User", user_id)
    json = request.get_json()
    if obj is not None:
        if json is not None:
            for key, value in json.items():
                if key not in ["id", "updated_at", "created_at", "email"]:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
