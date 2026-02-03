import unittest
import uuid
from app import create_app
from app.services import facade # استيراد الفاساد لضمان المزامنة

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        # تصفير البيانات لضمان بيئة نظيفة في كل اختبار (اختياري حسب تصميم المستودع)
        # facade.user_repo._storage = {} 

        # 1. إنشاء مستخدم فريد
        self.email = f"owner_{uuid.uuid4().hex[:6]}@test.com"
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": self.email
        })
        self.owner_id = user_res.get_json().get('id')
        
        # 2. إنشاء مرفق فريد
        amenity_res = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.amenity_id = amenity_res.get_json().get('id')

    def test_create_place_success(self):
        """اختبار إنشاء مكان بنجاح"""
        # نرسل طلب إنشاء المكان باستخدام الـ IDs التي حصلنا عليها
        response = self.client.post('/api/v1/places/', json={
            "title": "Luxury Apartment",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        
        # إذا فشل، اطبع الخطأ لنعرف السبب الحقيقي
        if response.status_code != 201:
            print(f"DEBUG: Response Error -> {response.get_json()}")
            
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_price(self):
        """اختبار منع السعر السالب"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cheap Room",
            "price": -50.0,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        # نتحقق من وجود كلمة price في رسالة الخطأ
        err_msg = str(response.get_json().get('error', '')).lower()
        self.assertIn("price", err_msg)

    def test_get_all_places(self):
        """اختبار جلب قائمة الأماكن"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_get_place_not_found(self):
        """اختبار جلب مكان غير موجود"""
        response = self.client.get('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)
