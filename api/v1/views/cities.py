#!/usr/bin/python3
""" module for states query """

from api.v1.views import app_views
from flask import jsonify, abort, request
import models


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates city"""
    obj = models.storage.get("State", state_id)
    if obj is None:
        abort(404)
    json = request.get_json()
    City = models.city.City
    if json is not None:
        if json.get("name") is not None:
            obj = City(name=json.get("name"), state_id=state_id)
            obj.save()
            return jsonify(obj.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def citiesId(state_id):
    """Returns the city with an id"""
    obj = models.storage.get("State", state_id)
    if obj is None:
        abort(404)
    all_cities = obj.cities
    new_dict = [val.to_dict() for val in all_cities]
    return jsonify(new_dict)


@app_views.route("/cities/<city_id>",
                 methods=["GET"], strict_slashes=False)
def retrieve_city(city_id):
    """Returns a city object"""
    obj = models.storage.get("City", city_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_del(city_id):
    """ return empty dict with 200 status"""
    obj = models.storage.get("City", city_id)
    if obj is not None:
        models.storage.delete(obj)
        models.storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Returns the city with an id"""
    obj = models.storage.get("City", city_id)
    json = request.get_json()
    if obj is not None:
        if json is not None:
            for key, value in json.items():
                if key not in ["id", "updated_at", "created_at",
                               "state_id"]:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
