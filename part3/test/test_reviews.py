import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place

@pytest.fixture
def client():
    app = create_app('config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # 1. إنشاء المستخدم (المقيّم)
            user = User(email="critic@hbnb.io", first_name="Critic", last_name="User")
            user.hash_password("pass123")
            db.session.add(user)
            db.session.flush()
            
            # 2. إنشاء مالك المكان
            owner = User(email="owner@hbnb.io", first_name="Owner", last_name="User")
            owner.hash_password("pass123")
            db.session.add(owner)
            db.session.flush()

            # 3. إنشاء المكان
            place = Place(
                title="Reviewable Place", 
                description="Nice place", 
                price=100.0, 
                latitude=1.0, 
                longitude=1.0, 
                owner_id=owner.id
            )
            db.session.add(place)
            db.session.commit()
            
            # تخزين المعرفات كأجزاء من الـ client لاستخدامها في الاختبار
            client.user_id = str(user.id)
            client.place_id = str(place.id)
            
            yield client
            db.session.remove()
            db.drop_all()

def test_create_review(client):
    """اختبار كتابة تقييم على مكان مع التأكد من أنواع البيانات"""
    # تسجيل الدخول
    login = client.post('/api/v1/auth/login', json={"email": "critic@hbnb.io", "password": "pass123"})
    token = login.get_json().get("access_token")
    
    # البيانات مع تحويل المعرفات لنصوص (Strings) كما طلب السيرفر
    review_data = {
        "text": "Amazing stay, very clean!", 
        "rating": 5,
        "user_id": client.user_id,
        "place_id": client.place_id
    }
    
    response = client.post('/api/v1/reviews/', 
                            json=review_data, 
                            headers={"Authorization": f"Bearer {token}"})
    
    # طباعة الخطأ إذا وجد للمساعدة
    if response.status_code != 201:
        print(f"\nDebug - Sent Data: {review_data}")
        print(f"Debug - Response: {response.get_json()}")
        
    assert response.status_code == 201
    assert response.get_json()["rating"] == 5
