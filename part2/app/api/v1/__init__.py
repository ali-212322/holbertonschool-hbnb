from flask import Blueprint
from flask_restx import Api

from app.api.v1.status import api as status_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_v1_bp)

api.add_namespace(status_ns, path="/status")
api.add_namespace(users_ns, path="/users")
api.add_namespace(places_ns, path="/places")
api.add_namespace(reviews_ns, path="/reviews")
api.add_namespace(amenities_ns, path="/amenities")
