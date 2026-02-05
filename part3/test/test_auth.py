import pytest
# استيراد db مباشرة من مكانه وتأخير استيراد create_app
from app import db 
import app as hbnb_app 
from app.models.user import User

@pytest.fixture
def client():
    # استدعاء create_app من داخل الموديول لتجنب الدائرة
    application = hbnb_app.create_app('config.TestingConfig') 
    
    with application.test_client() as client:
        with application.app_context():
            db.create_all()

            # زرع بيانات المستخدم
            if not User.query.filter_by(email="admin@hbnb.io").first():
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
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "admin1234"
    })
    
    if response.status_code != 200:
        print(f"\nResponse: {response.get_json()}")

    assert response.status_code == 200
    assert "access_token" in response.get_json()
