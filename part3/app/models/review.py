#!/usr/bin/python3
"""Review model"""

from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # يجب أن يكون النوع String(36) ليتوافق مع UUID في جداول User و Place
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    # استخدام back_populates يضمن الربط الصحيح مع الطرف الآخر من العلاقة
    # نستخدم اسم الكلاس كنص "Place" و "User" لتجنب الاستيراد الدائري (Circular Import)
    place = db.relationship("Place", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __init__(self, **kwargs):
        """
        Initialize Review
        نستخدم kwargs للسماح لـ SQLAlchemy و BaseModel بمعالجة البيانات تلقائياً
        """
        if 'rating' in kwargs:
            rating = kwargs.get('rating')
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("rating must be an integer between 1 and 5")
        
        if 'text' in kwargs:
            text = kwargs.get('text')
            if not text or not isinstance(text, str):
                raise ValueError("text must be a non-empty string")

        super().__init__(**kwargs)
