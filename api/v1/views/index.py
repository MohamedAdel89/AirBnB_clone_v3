#!/usr/bin/python3
"""
Module for index
"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route("/status")
def status():
    """Returns the status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Returns the stats"""
    classes = {"Amenity": "amenities", "City": "cities",
               "User": "users", "Place": "places",
               "Review": "reviews",
               "State": "states"}
    new_dict = map(lambda tpl: (tpl[1],
                                models.storage.count(tpl[0])),
                   classes.items())
    return jsonify(dict(new_dict))
