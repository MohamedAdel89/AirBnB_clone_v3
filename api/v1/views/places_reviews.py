#!/usr/bin/python3
""" module for place reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, request
import models


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def places_reviews(place_id):
    """Returns all the reviews"""
    obj = models.storage.get("Place", place_id)
    if obj is None:
        abort(404)
    new_dict = [val.to_dict() for val in obj.reviews]
    return jsonify(new_dict)


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def reviewId(review_id):
    """Returns the review with an id"""
    obj = models.storage.get("Review", review_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def review_del(review_id):
    """ return empty dict with 200 status"""
    obj = models.storage.get("Review", review_id)
    if obj is not None:
        models.storage.delete(obj)
        models.storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates review"""
    obj = models.storage.get("Place", place_id)
    if obj is None:
        abort(404)
    json = request.get_json()
    Review = models.review.Review
    if json is not None:
        user_id = json.get("user_id")
        if user_id is not None:
            text = json.get("text")
            if text is not None:
                obj = models.storage.get("User", user_id)
                if obj is not None:
                    obj = Review(place_id=place_id, user_id=user_id,
                                 text=text)
                    obj.save()
                    return jsonify(obj.to_dict()), 201
                else:
                    abort(404)
            else:
                abort(400, "Missing text")
        else:
            abort(400, "Missing user_id")
    else:
        abort(400, "Not a JSON")


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Returns the review with an id"""
    obj = models.storage.get("Review", review_id)
    json = request.get_json()
    if obj is not None:
        if json is not None:
            for key, value in json.items():
                if key not in ["id", "updated_at", "created_at",
                               "user_id", "place_id"]:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
