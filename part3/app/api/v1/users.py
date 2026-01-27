from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')


# Model for user creation (includes password)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Model for user update (admin can update email/password)
update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})


@api.route('/')
class UserList(Resource):

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Email already registered')
    def post(self):
        """Admin only: Create a new user"""
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        password = data.get('password')

        user_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email']
        }

        user = facade.create_user(user_data)
        user.hash_password(password)

        return {
            'id': user.id,
            'message': 'User created successfully'
        }, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get list of users"""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(update_user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid update')
    def put(self, user_id):
        """
        Update user:
        - Admin: can update any user (including email/password)
        - User: can update only himself (no email/password)
        """
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user_id = get_jwt_identity()

        data = api.payload

        # Non-admin users restrictions
        if not is_admin:
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password.'}, 400

        # Admin email uniqueness check
        if is_admin and 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404

        # Admin password update
        if is_admin and 'password' in data:
            user.hash_password(data['password'])

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
