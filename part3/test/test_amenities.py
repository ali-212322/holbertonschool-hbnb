import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def client():
    app = create_app('config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # حقن مستخدم أدمن لأن إنشاء المرافق غالباً ما يكون محصوراً بالأدمن
            admin = User(email="admin@hbnb.io", first_name="Admin", last_name="HBnB", is_admin=True)
            admin.hash_password("admin123")
            db.session.add(admin)
            db.session.commit()
            yield client
            db.session.remove()
            db.drop_all()

def test_create_amenity(client):
    """اختبار إنشاء مرفق جديد (مثل WiFi)"""
    # تسجيل دخول الأدمن
    login = client.post('/api/v1/auth/login', json={"email": "admin@hbnb.io", "password": "admin123"})
    token = login.get_json().get("access_token")
    
    response = client.post('/api/v1/amenities/', 
                            json={"name": "WiFi"}, 
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 201
    assert response.get_json()["name"] == "WiFi"
