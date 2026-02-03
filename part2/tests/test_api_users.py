import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """إعداد التطبيق وclient الاختبار قبل كل اختبار"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):
        """اختبار إنشاء مستخدم ببيانات صحيحة (201)"""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        response = self.client.post('/api/v1/users/', json=data)
        self.assertEqual(response.status_code, 201)
        
        json_data = response.get_json()
        self.assertIn('id', json_data)
        self.assertEqual(json_data['first_name'], "John")

    def test_create_user_invalid_email(self):
        """اختبار إنشاء مستخدم بإيميل خاطئ (400)"""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "bad-email-format"
        }
        response = self.client.post('/api/v1/users/', json=data)
        # يجب أن يعيد 400 لأن الـ Model سيرفض الإيميل
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_fields(self):
        """اختبار إرسال حقول فارغة"""
        data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "john@example.com"
        }
        response = self.client.post('/api/v1/users/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """اختبار جلب قائمة جميع المستخدمين (200)"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        """اختبار جلب مستخدم محدد بواسطة المعرف"""
        # أولاً ننشئ مستخدم لنحصل على ID
        create_res = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com"
        })
        user_id = create_res.get_json()['id']

        # نختبر الجلب
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['email'], "alice@example.com")
