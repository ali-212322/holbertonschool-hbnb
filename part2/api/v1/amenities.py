#!/usr/bin/env python3
"""
Amenity endpoints for HBnB API
"""

from flask_restx import Namespace, Resource, fields
from business_logic.amenity import Amenity
from persistence.in_memory_repository import InMemoryRepository

api = Namespace("amenities", description="Amenity operations")

repo = InMemoryRepository()

amenity_input = api.model("AmenityInput", {
    "name": fields.String(required=True),
})

amenity_output = api.model("AmenityOutput", {
    "id": fields.String,
    "name": fields.String,
})

def serialize_amenity(amenity):
    return {
        "id": amenity.id,
        "name": amenity.name,
    }

@api.route("/")
class AmenityList(Resource):

    @api.expect(amenity_input)
    @api.marshal_with(amenity_output, code=201)
    def post(self):
        data = api.payload
        amenity = Amenity(name=data.get("name"))
        repo.add(amenity)
        return serialize_amenity(amenity), 201

    @api.marshal_list_with(amenity_output)
    def get(self):
        amenities = repo.get_all()
        return [serialize_amenity(a) for a in amenities]

@api.route("/<string:amenity_id>")
class AmenityItem(Resource):

    @api.marshal_with(amenity_output)
    def get(self, amenity_id):
        amenity = repo.get(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return serialize_amenity(amenity)

