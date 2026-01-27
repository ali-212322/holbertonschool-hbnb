from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Request model
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})


@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Public: Get list of places"""
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'price': p.price
            }
            for p in places
        ], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created successfully')
    def post(self):
        """Protected: Create a new place"""
        current_user_id = get_jwt_identity()
        data = api.payload

        # Force owner from JWT
        data['owner_id'] = current_user_id

        place = facade.create_place(data)

        return {
            'id': place.id,
            'title': place.title,
            'owner_id': place.owner_id
        }, 201


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Public: Get place details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude
        }, 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Protected: Update place (owner or admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # ❌ Ownership check (admin bypass)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_place = facade.update_place(place_id, api.payload)

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'price': updated_place.price
        }, 200

    @jwt_required()
    def delete(self, place_id):
        """Protected: Delete place (owner or admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # ❌ Ownership check (admin bypass)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {}, 204
