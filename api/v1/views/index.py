#!/usr/bin/python3
"""
Create a route 'status' from the object 'app_views'
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def api_status():
    """
    Returns a json response for restful api status
    """
    response = {'status': 'OK'}
    return jsonify(response)

# Retrieve number of each object by type
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Returns the number of each object type
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
