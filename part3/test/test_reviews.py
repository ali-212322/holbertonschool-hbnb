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
            db.session.flush() # للحصول على الـ ID فوراً
            
            # 2. إنشاء مستخدم آخر ليكون صاحب المكان (لتجنب تعارض التقييم الذاتي إذا كان موجوداً)
            owner = User(email="owner@hbnb.io", first_name="Owner", last_name="User")
            owner.hash_password("pass123")
            db.session.add(owner)
            db.session.flush()

            # 3. إنشاء المكان الذي سيتم تقييمه
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
            
            yield client
            db.session.remove()
            db.drop_all()

def test_create_review(client):
    """اختبار كتابة تقييم على مكان"""
    # تسجيل الدخول
    login = client.post('/api/v1/auth/login', json={"email": "critic@hbnb.io", "password": "pass123"})
    token = login.get_json().get("access_token")
    
    # جربنا استخدام 'text' و 'comment' للتأكد من مسمى الحقل في مشروعك
    review_data = {
        "text": "Amazing stay, very clean!", # تأكد إذا كان مشروعك يستخدم 'comment' بدلاً من 'text'
        "rating": 5,
        "user_id": 1,
        "place_id": 1
    }
    
    response = client.post('/api/v1/reviews/', 
                            json=review_data, 
                            headers={"Authorization": f"Bearer {token}"})
    
    # إذا فشل، اطبع الرد لنعرف السبب (مثلاً حقل مفقود)
    if response.status_code != 201:
        print(f"\nReview Error Response: {response.get_json()}")
        
    assert response.status_code == 201
