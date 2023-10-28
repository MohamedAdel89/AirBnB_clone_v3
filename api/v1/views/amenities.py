#!/usr/bin/python3
""" module for amenities query """

from api.v1.views import app_views
from flask import jsonify, abort, request
import models


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Returns all the amenities"""
    all_amenity = models.storage.all("Amenity")
    new_dict = [val.to_dict() for val in all_amenity.values()]
    return jsonify(new_dict)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates amenity"""
    json = request.get_json()
    Amenity = models.amenity.Amenity
    if json is not None:
        if json.get("name") is not None:
            obj = Amenity(name=json.get("name"))
            obj.save()
            return jsonify(obj.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def amenityId(amenity_id):
    """Returns the amenity with an id"""
    obj = models.storage.get("Amenity", amenity_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_del(amenity_id):
    """ return empty dict with 200 status"""
    obj = models.storage.get("Amenity", amenity_id)
    if obj is not None:
        models.storage.delete(obj)
        models.storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Returns the amenity with an id"""
    obj = models.storage.get("Amenity", amenity_id)
    json = request.get_json()
    if obj is not None:
        if json is not None:
            for key, value in json.items():
                if key not in ["id", "updated_at", "created_at"]:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
