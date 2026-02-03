#!/usr/bin/python3
"""Amenity model"""

from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    # ملاحظة: تم حذف تعريف relationship هنا لأننا استخدمنا backref في ملف Place.
    # هذا يمنع الاستيراد الدائري تماماً ويسمح لك بالوصول لـ amenity.places برمجياً.

    def __init__(self, **kwargs):
        """Initialize Amenity"""
        # نتحقق من الاسم إذا تم تمريره يدوياً
        name = kwargs.get('name')
        if name:
            if not isinstance(name, str) or len(name) > 50:
                raise ValueError("name must be a string of max 50 characters")
        
        super().__init__(**kwargs)
