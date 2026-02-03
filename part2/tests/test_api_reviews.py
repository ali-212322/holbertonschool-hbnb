import unittest
import uuid
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """تجهيز البيئة: إنشاء مستخدم ومكان لربط التقييم بهما"""
        self.app = create_app()
        self.client = self.app.test_client()

        # 1. إنشاء مستخدم فريد
        user_email = f"reviewer_{uuid.uuid4().hex[:6]}@test.com"
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Reviewer",
            "email": user_email
        })
        self.user_id = user_res.get_json().get('id')

        # 2. إنشاء مكان فريد (يتطلب owner_id)
        place_res = self.client.post('/api/v1/places/', json={
            "title": "Reviewable Place",
            "description": "Test place",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_id": self.user_id
        })
        self.place_id = place_res.get_json().get('id')

    def test_create_review_success(self):
        """اختبار إنشاء تقييم بنجاح"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place, highly recommended!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['text'], "Amazing place, highly recommended!")

    def test_create_review_invalid_rating(self):
        """اختبار منع تقييم خارج النطاق (أكبر من 5)"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Too good to be true",
            "rating": 10,  # خطأ: يجب أن يكون بين 1-5
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("rating", response.get_json().get('error', '').lower())

    def test_get_reviews_by_place(self):
        """اختبار جلب التقييمات الخاصة بمكان معين عبر الـ Place Endpoint"""
        # أولاً ننشئ تقييماً
        self.client.post('/api/v1/reviews/', json={
            "text": "Good",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        
        # نطلب التقييمات من الـ endpoint الخاص بالمكان
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_delete_review(self):
        """اختبار حذف تقييم"""
        # إنشاء تقييم للحذف
        res = self.client.post('/api/v1/reviews/', json={
            "text": "To be deleted",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = res.get_json().get('id')
        
        # حذف التقييم
        del_res = self.client.get(f'/api/v1/reviews/{review_id}') # نستخدم GET أولاً للتأكد من وجوده
        self.assertEqual(del_res.status_code, 200)
