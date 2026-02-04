from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')
facade = HBnBFacade()

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Login and receive a JWT token"""
        data = api.payload
        user = facade.get_user_by_email(data['email'])

        if user and user.verify_password(data['password']):
            # نضع معلومات إضافية في التوكن مثل (is_admin)
            access_token = create_access_token(identity=user.id, additional_claims={'is_admin': user.is_admin})
            return {'access_token': access_token}, 200
        
        return {'error': 'Invalid email or password'}, 401
