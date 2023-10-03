#!/usr/bin/python3
"""
Creates a view for amenity object with default restful API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage

# Route to retrieve all amenity objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Get list of all amenity objects"""
    # Get all amenity objects from storage
    amenities = storage.all(Amenity).values()
    # Convert to dict and jsonify
    return jsonify([amenity.to_dict() for amenity in amenities])

# Route to retrieve specific amenity object by id
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get specified amenity object"""
    # Get amenity object with the specified ID from storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Return amenity object in JSON format
        return jsonify(amenity.to_dict())
    else:
        # Return 404 error
        abort(404)

# Route for deleting a specific amenity object
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity object specified"""
    # Get specified amenity object
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # Delete amenity object and save changes
        storage.delete(amenity)
        storage.save()
        # Return empty json with 200 status
        return jsonify({}), 200
    else:
        # Return 404 error
        abort(404)

# Route for creating a new amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create new amenity object"""
    if not request.get_json():
        # Return error if request is not a json
        abort(400, 'Not a JSON')

    # Get json data from the request
    data = request.get_json()
    if 'name' not in data:
        # Return 400 error
        abort(400, 'Missing name')

    # Create new amenity obj with given data, save to storage
    amenity = Amenity(**data)
    amenity.save()
    
    # Return newly created object
    return jsonify(amenity.to_dict()), 201

# Route for updating existing amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update amenity object by id"""
    # Get amenity object with the given id
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')
        # Get json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        # Save the updated amenity object to storage
        amenity.save()
        # Return the updated amenity object
        return jsonify(amenity.to_dict()), 200
    else:
        # Return 404 error if object is not found
        abort(404)

# Error handlers:
@app_views.errorhandler(404)
def not_found(error):
    """Return 404 not found error"""
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """Return 400 bad request error"""
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
