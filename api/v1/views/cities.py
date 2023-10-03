#!/usr/bin/python3
"""
Create a new view for city objects
"""
from flask import abort, jsonify, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage

# Route for retrieving all city objects for a specific state
@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves list of all city objects of a state
    """
    # Get state with given id from the storage
    state = storage.get(State, state_id)
    if not state:
        # Return 404 error
        abort(404)

    # Get all city objects associated with the state
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

# Retrieving a specific city object by id
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves city object
    """
    # Get city with the given id in the storage
    city = storage.get(City, city_id)
    if city:
        # Return city object in JSON format
        return jsonify(city.to_dict())
    else:
        # Return 404 error if object not found
        abort(404)

# Route for deleting specific city object by ID
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a city object
    """
    # Get city object with given id
    city = storage.get(City, city_id)
    if city:
        # Delete and save changes
        storage.delete(city)
        storage.save()
        # Return an empty dictionary with the status code 200
        return jsonify({}), 200
    else:
        # Return 404 error
        abort(404)

# Route to create a new city under a specific state
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create city under state with state_id given
    """
    # Get state
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # Check if request data is in JSON format
    if not request.get_json():
        # Return 400 error if dtat is not in JSON format
        abort(400, 'Not a JSON')
    # Get the JSON data from the request
    data = request.get_json()
    if 'name' not in data:
        # Return 400 error if name key is missing
        abort(400, 'Missing name')

    # Assign the 'state_id' key in the JSON data
    data['state_id'] = state_id
    # Create a new city object with the JSON data
    city = City(**data)
    # Save the city object to the storage
    storage.save(city)
    # Return new city object with 201 status code
    return jsonify(city.to_dict()), 201

# Route to update existing city object by ID
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object
    """
    # Get city object with the given ID
    city = storage.get(City, city_id)
    if city:
        # Check if data is json formatted
        if not request.get_json():
            # Return 400 error
            abort(400, 'Not a JSON')
        # Get json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        # Update attributes of the city object with the data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        # Save updated city
        city.save()
