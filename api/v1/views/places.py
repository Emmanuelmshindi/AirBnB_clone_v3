#!/usr/bin/python3
"""
Create a view for places objects - all default API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

# Route for retrieving all Place objects of a city
@app_views.route('/city/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_city(city_id):
    """List of all places by city specified"""
    # Get selected city from storage
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error if city is not found
        abort(404)
    # Get all place objects and convert to dictionaries
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

# Route for retrieving specific place by ID
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id):
    """List places by id"""
    # Get selected place by id
    place = storage.get(Place, place_id)
    if place:
        # Return place json
        return jsonify(place.to_dict())
    else:
        # Return 404 error
        abort(404)

# Route for deleting place object by id
@app_views.route('/places/<place_id>', method=['DELETE'])
def delete_place(place_id):
    """Delete place with specified id"""
    # Get selected place by id
    place = storage.get(Place, place_id)
    # Delete place and save
    if place:
        storage.delete(place)
        storage.save()
        # Return empty json
        return jsonify({}), 200
    else:
        # Return 404 error
        abort(404)

# Route for creating a new place object
@app_views.route('/city/<city_id>/places', method=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create place under city specified"""
    # Get specified city
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error
        abort(404)

    # Check if request data is json format
    if not request.get_json():
        abort(400, 'Not a JSON')

    # Get json data from request
    data = request.get_json()
    if 'user_id' not in data:
        # Return 400 error if user_id is missing
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    # Get user object with the given user id
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    # Assign city_id to the json data
    data['city_id'] = city_id
    # Create new json object with the JSON data
    place = Place(**data)
    # Save the place object to storage
    place.save()
    # Return the newly created object
    return jsonify(place.to_dict()), 201

# Route for updating existing place object by id
@app_views.route('/place/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update place by id"""
    # Get specified place
    place = storage.get(Place, place_id)
    if place:
        # Check if data is in json format
        if not request.get_json():
            abort(400, 'Not a JSON')

        # Get json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        # Update attributes of the place object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        # Save the updated place object
        place.save()
        # Return updated place object
        return jsonify(place.to_dict()), 200
    else:
        abort(404)

# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''
    Returns 404: Not Found
    '''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''
    Return Bad Request message for illegal requests to the API
    '''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
