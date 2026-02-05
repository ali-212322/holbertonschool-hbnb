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
            # حقن مستخدم الاختبار
            admin_user = User(
                email="admin@hbnb.io",
                first_name="Admin",
                last_name="HBnB",
                is_admin=True
            )
            admin_user.hash_password("admin1234")
            db.session.add(admin_user)
            db.session.commit()

            yield client

            db.session.remove()
            db.drop_all()

def test_login_success(client):
    """اختبار تسجيل الدخول الناجح"""
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "admin1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_wrong_password(client):
    """اختبار تسجيل الدخول بكلمة مرور خاطئة"""
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "wrongpassword"
    })
    # يجب أن يرفض النظام الدخول
    assert response.status_code == 401
    assert response.get_json().get("msg") == "Bad email or password"

def test_login_invalid_user(client):
    """اختبار تسجيل الدخول بمستخدم غير موجود"""
    response = client.post('/api/v1/auth/login', json={
        "email": "nonexistent@hbnb.io",
        "password": "password123"
    })
    assert response.status_code == 401
