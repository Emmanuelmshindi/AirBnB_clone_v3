#!/usr/bin/python3
"""
Create new view for review objects - Handles all default restful api calls
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage

# Route for retrieving all review objects of a place
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Get list of all review objects by place
    """
    # Get specified place
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error
        abort(404)

    # Get all reviews for the place and convert to dictionary
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

# Route for retrieving specific review object by id
@app_views.route('/reviews/review_id', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get specified review object"""
    # Get review with passed id
    review = storage.get(Review, review_id)
    if review:
        # Return the Review object in JSON format
        return jsonify(review.to_dict())
    else:
        # Return 404 error if the Review object is not found
        abort(404)

# Route for deleting a specified review object by id
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete review by id"""
    # Get selected review from storage
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})

# Route for creating a new review object
@app_views.route('/places/place_id/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create new review for specified place"""
    # Get place
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    # Check if request data is in JSON format
    if not request.get_json():
        abort(400, 'Not a JSON')

    # Get JSON data from the request
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')

    # Get user object with the given user_id from storage
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    # Assign the place id to the data
    data['place_id'] = place_id
    # Create new review object with the given data
    review = Review(**data)
    # Save review object
    review.save()
    # Return new review object as JSON
    return jsonify(review.to_dict()), 201

# Route for updating existing review object by ID
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""
    # Get review object specified from storage
    review = storage.get(Review, review_id)
    if review:
        # Check if request data is in JSON format
        if not request.get_json():
            abort(404, 'Not a JSON')

        # Get data from request
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        # Update the selected review with the data in the request
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        # Save the updated review object to storage
        review.save()

        # Return update review object in json format with 200 status
        return jsonify(review.to_dict()), 200
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
