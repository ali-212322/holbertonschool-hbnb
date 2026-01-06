#!/usr/bin/env python3
"""
HBnB API - Flask application entry point
"""

from flask import Flask
from flask_restx import Api

# Import namespaces
from api.v1.users import api as users_ns
from api.v1.places import api as places_ns
from api.v1.reviews import api as reviews_ns
from api.v1.amenities import api as amenities_ns

app = Flask(__name__)

# Initialize Flask-RESTx API
api = Api(
    app,
    version="1.0",
    title="HBnB API",
    description="HBnB RESTful API"
)

# Register namespaces
api.add_namespace(users_ns, path="/api/v1/users")
api.add_namespace(places_ns, path="/api/v1/places")
api.add_namespace(reviews_ns, path="/api/v1/reviews")
api.add_namespace(amenities_ns, path="/api/v1/amenities")
# Optional health check (خارج Swagger)
@app.route("/status")
def status():
    return {"status": "HBnB API running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
