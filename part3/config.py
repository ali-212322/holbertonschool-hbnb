import os

# تحديد المجلد الرئيسي للمشروع للحصول على مسار مطلق لقاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # مسار قاعدة بيانات التطوير
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'development.db')

# --- التحديث الجديد هنا ---
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # استخدام قاعدة بيانات في الذاكرة (In-memory) تجعل الاختبارات سريعة ولا تترك ملفات خلفها
    SQLALCHEMY_DATABASE_URI = 'sqlite://' 

# قاموس لتسهيل استدعاء الإعدادات حسب البيئة
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
# -------------------------
