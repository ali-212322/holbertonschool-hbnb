"""
Comprehensive Unit Tests for HBnB API
Uses pytest for automated testing
Run with: pytest test_api.py -v
"""

from hbnb.app.services.facade import HBnBFacade
from hbnb.app import create_app
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def facade():
    """Create a fresh facade instance for each test."""
    return HBnBFacade()


# ==================== USER TESTS ====================

class TestUserEndpoints:
    """Test suite for User endpoints"""

    def test_create_user_success(self, client):
        """Test successful user creation"""
        response = client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'is_admin': False
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['first_name'] == 'John'
        assert data['email'] == 'john.doe@example.com'

    def test_create_user_duplicate_email(self, client):
        """Test creating user with duplicate email"""
        user_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'duplicate@example.com',
            'is_admin': False
        }
        # Create first user
        client.post('/api/v1/users/', json=user_data)
        # Try to create duplicate
        response = client.post('/api/v1/users/', json=user_data)
        assert response.status_code == 409

    def test_create_user_invalid_email(self, client):
        """Test creating user with invalid email"""
        response = client.post('/api/v1/users/', json={
            'first_name': 'Invalid',
            'last_name': 'User',
            'email': 'not-an-email',
            'is_admin': False
        })
        assert response.status_code == 400

    def test_get_all_users(self, client):
        """Test retrieving all users"""
        response = client.get('/api/v1/users/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_get_user_by_id(self, client):
        """Test retrieving a specific user"""
        # Create user first
        create_response = client.post('/api/v1/users/', json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com',
            'is_admin': False
        })
        user_id = create_response.get_json()['id']

        # Retrieve user
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == user_id

    def test_get_nonexistent_user(self, client):
        """Test retrieving a non-existent user"""
        response = client.get('/api/v1/users/nonexistent-id')
        assert response.status_code == 404

    def test_update_user(self, client):
        """Test updating user information"""
        # Create user
        create_response = client.post('/api/v1/users/', json={
            'first_name': 'Update',
            'last_name': 'Test',
            'email': 'update.test@example.com',
            'is_admin': False
        })
        user_id = create_response.get_json()['id']

        # Update user
        response = client.put(f'/api/v1/users/{user_id}', json={
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated.email@example.com',
            'is_admin': True
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Updated'
        assert data['is_admin'] == True


# ==================== AMENITY TESTS ====================

class TestAmenityEndpoints:
    """Test suite for Amenity endpoints"""

    def test_create_amenity_success(self, client):
        """Test successful amenity creation"""
        response = client.post('/api/v1/amenities/', json={
            'name': 'WiFi'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['name'] == 'WiFi'

    def test_create_amenity_duplicate_name(self, client):
        """Test creating amenity with duplicate name"""
        amenity_data = {'name': 'Duplicate Amenity'}
        client.post('/api/v1/amenities/', json=amenity_data)
        response = client.post('/api/v1/amenities/', json=amenity_data)
        assert response.status_code == 409

    def test_create_amenity_empty_name(self, client):
        """Test creating amenity with empty name"""
        response = client.post('/api/v1/amenities/', json={'name': ''})
        assert response.status_code == 400

    def test_get_all_amenities(self, client):
        """Test retrieving all amenities"""
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_update_amenity(self, client):
        """Test updating amenity"""
        # Create amenity
        create_response = client.post('/api/v1/amenities/', json={
            'name': 'Original Name'
        })
        amenity_id = create_response.get_json()['id']

        # Update amenity
        response = client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': 'Updated Name'
        })
        assert response.status_code == 200
        assert response.get_json()['name'] == 'Updated Name'


# ==================== PLACE TESTS ====================

class TestPlaceEndpoints:
    """Test suite for Place endpoints"""

    @pytest.fixture
    def test_user(self, client):
        """Create a test user for place tests"""
        response = client.post('/api/v1/users/', json={
            'first_name': 'Place',
            'last_name': 'Owner',
            'email': 'place.owner@example.com',
            'is_admin': False
        })
        return response.get_json()

    def test_create_place_success(self, client, test_user):
        """Test successful place creation"""
        response = client.post('/api/v1/places/', json={
            'title': 'Beautiful Apartment',
            'description': 'A lovely place to stay',
            'price': 150.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': test_user['id'],
            'amenities': []
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['title'] == 'Beautiful Apartment'
        assert data['price'] == 150.0

    def test_create_place_invalid_price(self, client, test_user):
        """Test creating place with negative price"""
        response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': -50.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': test_user['id'],
            'amenities': []
        })
        assert response.status_code == 400

    def test_create_place_invalid_latitude(self, client, test_user):
        """Test creating place with invalid latitude"""
        response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 95.0,  # Out of range
            'longitude': -74.0060,
            'owner_id': test_user['id'],
            'amenities': []
        })
        assert response.status_code == 400

    def test_create_place_invalid_longitude(self, client, test_user):
        """Test creating place with invalid longitude"""
        response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': 200.0,  # Out of range
            'owner_id': test_user['id'],
            'amenities': []
        })
        assert response.status_code == 400

    def test_create_place_nonexistent_owner(self, client):
        """Test creating place with non-existent owner"""
        response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': 'nonexistent-id',
            'amenities': []
        })
        assert response.status_code == 404


# ==================== REVIEW TESTS ====================

class TestReviewEndpoints:
    """Test suite for Review endpoints"""

    @pytest.fixture
    def test_setup(self, client):
        """Create test user and place for review tests"""
        # Create user
        user_response = client.post('/api/v1/users/', json={
            'first_name': 'Reviewer',
            'last_name': 'User',
            'email': 'reviewer@example.com',
            'is_admin': False
        })
        user = user_response.get_json()

        # Create place
        place_response = client.post('/api/v1/places/', json={
            'title': 'Review Test Place',
            'description': 'Place for testing reviews',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': user['id'],
            'amenities': []
        })
        place = place_response.get_json()

        return {'user': user, 'place': place}

    def test_create_review_success(self, client, test_setup):
        """Test successful review creation"""
        response = client.post('/api/v1/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'user_id': test_setup['user']['id'],
            'place_id': test_setup['place']['id']
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['rating'] == 5

    def test_create_review_invalid_rating(self, client, test_setup):
        """Test creating review with invalid rating"""
        response = client.post('/api/v1/reviews/', json={
            'text': 'Test review',
            'rating': 6,  # Out of range (1-5)
            'user_id': test_setup['user']['id'],
            'place_id': test_setup['place']['id']
        })
        assert response.status_code == 400

    def test_create_review_empty_text(self, client, test_setup):
        """Test creating review with empty text"""
        response = client.post('/api/v1/reviews/', json={
            'text': '',
            'rating': 5,
            'user_id': test_setup['user']['id'],
            'place_id': test_setup['place']['id']
        })
        assert response.status_code == 400

    def test_update_review(self, client, test_setup):
        """Test updating review"""
        # Create review
        create_response = client.post('/api/v1/reviews/', json={
            'text': 'Original review',
            'rating': 3,
            'user_id': test_setup['user']['id'],
            'place_id': test_setup['place']['id']
        })
        review_id = create_response.get_json()['id']

        # Update review
        response = client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Updated review',
            'rating': 5,
            'user_id': test_setup['user']['id'],
            'place_id': test_setup['place']['id']
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['text'] == 'Updated review'
        assert data['rating'] == 5

    def test_delete_review(self, client, test_setup):
        """Test deleting review"""
        # Create review
        create_response = client.post('/api/v1/reviews/', json={
            'text': 'Review to delete',
            'rating': 4,
            'user_id': test_setup['user']['id'],
            'place_id': test_setup['place']['id']
        })
        review_id = create_response.get_json()['id']

        # Delete review
        response = client.delete(f'/api/v1/reviews/{review_id}')
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(f'/api/v1/reviews/{review_id}')
        assert get_response.status_code == 404

    def test_get_reviews_by_place(self, client, test_setup):
        """Test getting all reviews for a place"""
        # Create multiple reviews
        for i in range(3):
            client.post('/api/v1/reviews/', json={
                'text': f'Review {i+1}',
                'rating': i + 3,
                'user_id': test_setup['user']['id'],
                'place_id': test_setup['place']['id']
            })

        # Get reviews for place
        response = client.get(
            f'/api/v1/reviews/places/{test_setup["place"]["id"]}/reviews'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 3


# ==================== VALIDATION TESTS ====================

class TestValidations:
    """Test suite for model validations"""

    def test_user_email_validation(self, facade):
        """Test user email format validation"""
        with pytest.raises(ValueError, match="email must be a valid email address"):
            facade.create_user({
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'invalid-email',
                'is_admin': False
            })

    def test_user_name_length_validation(self, facade):
        """Test user name length validation"""
        with pytest.raises(ValueError):
            facade.create_user({
                'first_name': 'A' * 51,  # Too long
                'last_name': 'User',
                'email': 'test@example.com',
                'is_admin': False
            })

    def test_place_price_validation(self, facade):
        """Test place price validation"""
        # First create a user
        user = facade.create_user({
            'first_name': 'Owner',
            'last_name': 'Test',
            'email': 'owner@test.com',
            'is_admin': False
        })

        with pytest.raises(ValueError, match="price must be a positive number"):
            facade.create_place({
                'title': 'Test',
                'description': 'Test',
                'price': -100.0,
                'latitude': 40.0,
                'longitude': -70.0,
                'owner_id': user.id,
                'amenities': []
            })

    def test_review_rating_validation(self, facade):
        """Test review rating validation"""
        # Create user and place
        user = facade.create_user({
            'first_name': 'User',
            'last_name': 'Test',
            'email': 'user@test.com',
            'is_admin': False
        })

        place = facade.create_place({
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -70.0,
            'owner_id': user.id,
            'amenities': []
        })

        with pytest.raises(ValueError, match="rating must be between 1 and 5"):
            facade.create_review({
                'text': 'Test review',
                'rating': 10,  # Invalid
                'user_id': user.id,
                'place_id': place.id
            })


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
