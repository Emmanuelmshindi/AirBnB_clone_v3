#!/usr/bin/python3
"""
Create e new view for state objects.All default RESTAPI functions
"""
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage

# Route to retrieve all state objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all state objects
    """
    # Get all states from storage
    states = storage.all(State).values()
    # Convert them to json
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

# Retrieve single state by id
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a single state by id
    """
    # Retrieve the single state from storage
    state = storage.get(State, state_id)
    if state:
        # Return state object in json
        return jsonify(state.to_dict())
    else:
        # Raise 404 error
        abort(404)

# Delete specific state object by id
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes state object by id
    """
    # Get state with given id
    state = storage.get(State, state_id)
    if state:
        # Delete the given state and save changes
        storage.delete(state)
        storage.save()
        # Return empty json with state 200
        return jsonify({}), 200
    else:
        # Return 404 error
        abort(404)

# Route to create new state object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a state object
    """
    if not request.get_json():
        # Return 400 error if request not in json format
        abort(400, 'Not a JSON')
    # Get json data from request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # Return 400 error if 'name' key is missing in JSON data
        abort(400, 'Missing name')

    # Create a new state object with the new JSON data
    state = State(**kwargs)
    # Save state object to storage
    state.save()
    # Return newly created state object in JSON format
    return jsonify(state.to_dict()), 201

# Route for updating state object by id
@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def update_state(state_id):
    """
    Updates state by id
    """
    # Get state with the give ID
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            # Return 400 error if request data is not in JSON  format
            abort(400, 'Not a JSON')
        # Get JSON data from state
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update attributes of state object with JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        # Save updated state to storage
        state.save()
        # Return update state object in JSON format with 200 status code
        return jsonify(state.to_dict()), 200
    else:
        # Return 404 error if object not found
        abort(404)

# Error handlers:
@app_views.errorhandler(404)
def not_found(error):
    """
    Raises a 404 error
    """
    # Return json response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """
    Raises a 400 error
    """
    # Return reponse for 400 error
    response = {'error': 'Bad request'}
    return jsonify(response), 400
