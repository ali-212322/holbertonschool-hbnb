#!/usr/bin/env python3
"""
Place endpoints for HBnB API (Task 5)
Includes reviews collection for each place.
"""

from flask_restx import Namespace, Resource, fields
from business_logic.facade import facade

api = Namespace("places", description="Place operations")

# ---------- Swagger Models ----------
place_input = api.model("PlaceInput", {
    "name": fields.String(required=True),
    "owner_id": fields.String(required=True),
    "description": fields.String(required=False),
    "price": fields.Float(required=False),
    "latitude": fields.Float(required=False),
    "longitude": fields.Float(required=False),
})

review_small = api.model("ReviewSmall", {
    "id": fields.String,
    "text": fields.String,
    "user_id": fields.String,
    "place_id": fields.String,
})

place_output = api.model("PlaceOutput", {
    "id": fields.String,
    "name": fields.String,
    "owner_id": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "amenities": fields.List(fields.String),
    "reviews": fields.List(fields.Nested(review_small)),
    "created_at": fields.String,
    "updated_at": fields.String,
})


def serialize_review_small(r):
    return {
        "id": r.id,
        "text": r.text,
        "user_id": r.user_id,
        "place_id": r.place_id,
    }


def serialize_place(p):
    # Get reviews for this place (Task 5 requirement)
    try:
        reviews = facade.list_reviews_by_place(p.id)
    except ValueError:
        reviews = []

    return {
        "id": p.id,
        "name": p.name,
        "owner_id": p.owner_id,
        "description": p.description,
        "price": p.price,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "amenities": p.amenities,
        "reviews": [serialize_review_small(r) for r in reviews],
        "created_at": p.created_at.isoformat(),
        "updated_at": p.updated_at.isoformat(),
    }


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_input)
    @api.marshal_with(place_output, code=201)
    def post(self):
        data = api.payload
        try:
            p = facade.create_place(
                name=data.get("name"),
                owner_id=data.get("owner_id"),
                description=data.get("description", ""),
                price=data.get("price", 0.0),
                latitude=data.get("latitude", None),
                longitude=data.get("longitude", None),
            )
        except ValueError as e:
            api.abort(400, str(e))
        return serialize_place(p), 201

    @api.marshal_list_with(place_output)
    def get(self):
        return [serialize_place(p) for p in facade.list_places()]


@api.route("/<string:place_id>")
class PlaceItem(Resource):
    @api.marshal_with(place_output)
    def get(self, place_id):
        p = facade.get_place(place_id)
        if not p:
            api.abort(404, "Place not found")
        return serialize_place(p)

    @api.expect(place_input)
    @api.marshal_with(place_output)
    def put(self, place_id):
        data = api.payload
        p = facade.update_place(
            place_id,
            name=data.get("name"),
            owner_id=data.get("owner_id"),
            description=data.get("description", ""),
            price=data.get("price", 0.0),
            latitude=data.get("latitude", None),
            longitude=data.get("longitude", None),
        )
        if not p:
            api.abort(404, "Place not found")
        return serialize_place(p), 200
