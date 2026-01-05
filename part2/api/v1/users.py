#!/usr/bin/env python3
"""
User endpoints for HBnB API
"""

from flask_restx import Namespace, Resource, fields
from business_logic.user import User
from persistence.in_memory_repository import InMemoryRepository

# Namespace
api = Namespace("users", description="User operations")

# In-memory repository (مؤقتًا)
repo = InMemoryRepository()

# Swagger models
user_input = api.model("UserInput", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

user_output = api.model("UserOutput", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
})

def serialize_user(user):
    """Return user dict without password"""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }

@api.route("/")
class UserList(Resource):
    @api.expect(user_input)
    @api.marshal_with(user_output, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
        )
        repo.add(user)
        return serialize_user(user), 201

    @api.marshal_list_with(user_output)
    def get(self):
        """Get all users"""
        users = repo.get_all()
        return [serialize_user(u) for u in users]

@api.route("/<string:user_id>")
class UserItem(Resource):
    @api.marshal_with(user_output)
    def get(self, user_id):
        """Get a user by ID"""
        user = repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
        return serialize_user(user)

    @api.expect(user_input)
    @api.marshal_with(user_output)
    def put(self, user_id):
        """Update a user"""
        user = repo.get(user_id)
        if not user:
            api.abort(404, "User not found")

        data = api.payload
        user.update(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
        )
        return serialize_user(user)

