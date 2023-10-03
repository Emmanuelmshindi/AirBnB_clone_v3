#!/usr/bin/python3
"""
Create flask app register blueprint app_views with flask instance 'app'
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
# Enable CORS
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

# Register the app_views blueprint
app.register_blueprint(app_views)
app.url.strict_slashes = False

# Teardown function to close SQLAlchemy session
@app.teardown_appcontext
def teardown_engine(exception):
    """
    Removes current sqlalchemy session after each request
    """
    storage.close()

# 404 error page
@app.errorhandler(404)
def error_page(error):
    """
    Return json response with "not found" error message
    """
    response = {"error": "Not found"}
    return jsonify(response), 404

if __name__ == '__main__':
    # Get host and port from env variables
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
