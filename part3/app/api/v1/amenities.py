from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# تعريف نموذج البيانات للمرافق
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity (e.g., WiFi, Pool)')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    def post(self):
        """Create a new amenity"""
        data = api.payload
        amenity = facade.create_amenity(data)
        return {'id': amenity.id, 'name': amenity.name}, 201

    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200
