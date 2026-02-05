import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place

@pytest.fixture
def client():
    # استخدام إعدادات الاختبار
    app = create_app('config.TestingConfig') 
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # 1. زرع مستخدم مسؤول ليكون هو "صاحب المكان"
            owner = User(
                email="owner@hbnb.io",
                first_name="Owner",
                last_name="User",
                is_admin=False
            )
            owner.hash_password("password123")
            db.session.add(owner)
            db.session.commit()

            yield client

            db.session.remove()
            db.drop_all()

def test_create_place_success(client):
    """اختبار إنشاء مكان جديد بنجاح باستخدام التوكن"""
    
    # الخطوة الأولى: تسجيل الدخول للحصول على التوكن
    login_response = client.post('/api/v1/auth/login', json={
        "email": "owner@hbnb.io",
        "password": "password123"
    })
    access_token = login_response.get_json().get("access_token")
    
    # الخطوة الثانية: إرسال طلب إنشاء المكان مع التوكن في الـ Headers
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    place_data = {
        "title": "Luxury Apartment",
        "description": "A beautiful place to stay",
        "price": 150.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": 1  # نستخدم المعرف الخاص بالمستخدم الذي أنشأناه
    }
    
    response = client.post('/api/v1/places/', json=place_data, headers=headers)
    
    # التحقق من النتيجة
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Luxury Apartment"
    assert "id" in data

def test_create_place_unauthorized(client):
    """اختبار منع إنشاء مكان بدون توكن"""
    place_data = {
        "title": "Unauthorized Place",
        "description": "Should fail",
        "price": 100.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": 1
    }
    
    response = client.post('/api/v1/places/', json=place_data)
    
    # يجب أن يرفض الطلب لأن التوكن مفقود
    assert response.status_code == 401
