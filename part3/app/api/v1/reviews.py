from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Request model - أضفنا الـ rating هنا ليتوافق مع قاعدة البيانات
review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5)
})

@api.route('/')
class ReviewList(Resource):

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'place_id': r.place_id,
                'user_id': r.user_id
            } for r in facade.get_all_reviews()
        ], 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid review or business logic error')
    @api.response(404, 'Place not found')
    def post(self):
        """Create a review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        data = api.payload

        # 1. التحقق من وجود المكان
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        # 2. منع المستخدم من تقييم مكانه الخاص (إلا إذا كان أدمن)
        if not is_admin and place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place.'}, 400

        # 3. منع تكرار التقييم لنفس المكان من نفس الشخص
        all_reviews = facade.get_all_reviews()
        for review in all_reviews:
            if review.place_id == data['place_id'] and review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place.'}, 400

        # 4. إنشاء التقييم عبر الـ facade
        review = facade.create_review(data)

        return {
            'id': review.id,
            'message': 'Review created successfully'
        }, 201

@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id
        }, 200

    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (owner or admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_review = facade.update_review(review_id, api.payload)
        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner or admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
