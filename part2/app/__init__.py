from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
# إذا لم تنشئ ملف status.py بعد، قم بتعطيل السطرين الخاصين به
# from app.api.v1.status import api as status_ns 

def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',  # هذا يحدد أين ستجد صفحة Swagger
    )

    # تسجيل الـ namespaces مع إضافة البادئة الصحيحة للمسارات
    # لاحظ أننا أضفنا /api/v1 لكي تتطابق مع طلبات الاختبار cURL
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # api.add_namespace(status_ns, path='/api/v1/status')

    return app
