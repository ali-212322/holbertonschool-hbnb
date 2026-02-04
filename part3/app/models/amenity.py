#!/usr/bin/python3
"""Amenity model"""

from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, **kwargs):
        """
        Initialize Amenity with proper validation
        """
        name = kwargs.get('name')
        if name is not None:
            # التأكد من أنه نص وليس فارغاً ولا يتجاوز 50 حرفاً
            if not isinstance(name, str) or len(name.strip()) == 0 or len(name) > 50:
                raise ValueError("name must be a non-empty string of max 50 characters")
            kwargs['name'] = name.strip()

        super().__init__(**kwargs)
