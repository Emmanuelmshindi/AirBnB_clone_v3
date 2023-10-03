#!/usr/bin/python3
"""
Create a new view for user objects, handles all default restapi actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


# Route for retrieving all user objects
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Return all user objects"""
    # Get all user objects and convert to dictionaries
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

# Route for retrieving specific user object by ID
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieve user by id """
    # Find user with specified id
    user = storage.get(User, user_id)
    if user:
        # Return user object in json
        return jsonify(user.to_dict())
    else:
        # Return 404 error if object is not found
        abort(404)

# Deleting specific user object by ID
@app_views.route('/users/user_id', methods=['DELETE'])
def delete_user(user_id):
    """Delete user by ID"""
    # Find user with specified ID
    user = storage.get(User, user_id)
    if user:
        # Delete user and save
        storage.delete(user)
        storage.save()
        # Return empty json and 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if object is not found
        abort(404)

# Route for creating new user object
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create new user"""
    # Check if request data is in json format
    if not request.get_json():
        # Return 404 error
        abort(400, 'Not a JSON')

    # Get json data from the request
    data = request.get_json()
    if 'email' not in data:
        # Return 400 error if email key is missing
        abort(400, 'Missing email')

    if 'password' not in data:
        # Return 400 error
        abort(400, 'Missing password')

    # Create new user with the json data passed
    user = User(**data)
    user.save()
    # Return json with created user data
    return jsonify(user.to_dict()), 201

# Route for updating existing user object by ID
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update selected user"""
    # Get specified user by ID provided
    user = storage.get(User, user_id)
    if user:
        # Check if request is in json form
        if not request.get_json():
            # Return 400 error
            abort(400, 'Not a JSON')
        # Get json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        # Update the attributes of the json data with the json attributes
        for key,value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        # Save updated user object and return json of the object
        user.save()
        return jsonify(user.to_dict()), 201
    else:
        # Return error 404 if object is not found
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
    Return Bad Request
    '''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
