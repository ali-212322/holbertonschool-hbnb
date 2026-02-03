import unittest
import uuid
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # استخدام إيميل فريد لكل اختبار لتجنب خطأ "Email already registered"
        unique_email = f"user_{uuid.uuid4()}@example.com"
        
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "John", 
            "last_name": "Doe", 
            "email": unique_email
        })
        
        user_data = user_res.get_json()
        self.owner_id = user_data.get('id')

        # إنشاء مرفق
        amenity_res = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.amenity_id = amenity_res.get_json().get('id')

    def test_create_place_success(self):
        """اختبار إنشاء مكان بنجاح"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Luxury Apartment",
            "description": "A beautiful place to stay",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_price(self):
        """اختبار منع السعر السالب"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cheap Room",
            "price": -10.0,
            "latitude": 0, 
            "longitude": 0,
            "owner_id": self.owner_id
        })
        # نتوقع 400 بسبب السعر السالب
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price must be a number", response.get_json().get('error', ''))

    def test_get_all_places(self):
        """اختبار جلب قائمة الأماكن"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_get_place_not_found(self):
        """اختبار جلب مكان غير موجود"""
        response = self.client.get('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)
