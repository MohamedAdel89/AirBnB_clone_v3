#!/usr/bin/python3
""" module for place - amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
import models


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def places_amenities(place_id):
    """Returns all the amenities"""
    obj = models.storage.get("Place", place_id)
    if obj is None:
        abort(404)
    if models.storage_t == 'db':
        new_dict = [val.to_dict() for val in obj.amenities]
        return jsonify(new_dict)
    else:
        new_dict = [val.to_dict() for val in obj.amenity_ids]
        return jsonify(new_dict)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def places_amenities_del(place_id, amenity_id):
    """ return empty dict with 200 status"""
    obj_place = models.storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    obj_amenity = models.storage.get("Amenity", amenity_id)
    if obj_amenity is None:
        abort(404)
    if models.storage_t == 'db':
        if obj_amenity not in obj_place.amenities:
            abort(404)
        else:
            obj_place.amenities.remove(obj_amenity)
    else:
        if obj_amenity not in obj_place.amenity_ids:
            abort(404)
        else:
            obj_place.amenity_ids.remove(obj_amenity)
    models.storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def create_place_amenities(place_id, amenity_id):
    """Creates amenity for a place"""
    obj_place = models.storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    obj_amenity = models.storage.get("Amenity", amenity_id)
    if obj_amenity is None:
        abort(404)
    if obj_amenity in obj_place:
        return jsonify(obj_amenity.to_dict())
    if models.storage_t == 'db':
        if obj_amenity not in obj_place.amenities:
            abort(404)
        else:
            obj_place.amenities.append(obj_amenity)
    else:
        if obj_amenity not in obj_place.amenity_ids:
            abort(404)
        else:
            obj_place.amenity_ids.append(obj_amenity)
    obj_place.save()
    return jsonify(obj_amenity.to_dict()), 201
