#!/usr/bin/env python3
"""
Review endpoints for HBnB API (Task 5)
"""

from flask_restx import Namespace, Resource, fields
from business_logic.facade import facade

api = Namespace("reviews", description="Review operations")

# ---------- Swagger Models ----------
review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
})

review_output = api.model("ReviewOutput", {
    "id": fields.String,
    "text": fields.String,
    "user_id": fields.String,
    "place_id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})


def serialize_review(r):
    """Convert Review object to dict"""
    return {
        "id": r.id,
        "text": r.text,
        "user_id": r.user_id,
        "place_id": r.place_id,
        "created_at": r.created_at.isoformat(),
        "updated_at": r.updated_at.isoformat(),
    }


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_input)
    @api.marshal_with(review_output, code=201)
    def post(self):
        """Create a new review"""
        data = api.payload
        try:
            r = facade.create_review(
                text=data.get("text"),
                user_id=data.get("user_id"),
                place_id=data.get("place_id"),
            )
        except ValueError as e:
            api.abort(400, str(e))
        return serialize_review(r), 201

    @api.marshal_list_with(review_output)
    def get(self):
        """Get all reviews"""
        return [serialize_review(r) for r in facade.list_reviews()]


@api.route("/<string:review_id>")
class ReviewItem(Resource):
    @api.marshal_with(review_output)
    def get(self, review_id):
        """Get one review"""
        r = facade.get_review(review_id)
        if not r:
            api.abort(404, "Review not found")
        return serialize_review(r)

    @api.expect(review_input)
    @api.marshal_with(review_output)
    def put(self, review_id):
        """Update a review"""
        data = api.payload
        try:
            r = facade.update_review(
                review_id,
                text=data.get("text"),
                user_id=data.get("user_id"),
                place_id=data.get("place_id"),
            )
        except ValueError as e:
            api.abort(400, str(e))

        if not r:
            api.abort(404, "Review not found")

        return serialize_review(r), 200

    def delete(self, review_id):
        """Delete a review (Task 5)"""
        deleted_obj = facade.delete_review(review_id)  # repo returns object or None
