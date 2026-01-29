#!/usr/bin/python3
"""Amenity model"""

from app import db
from app.models.base_model import BaseModel
from app.models.place import place_amenity
from sqlalchemy.orm import relationship

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
        lazy="subquery"
    )

    def __init__(self, name):
        super().__init__()

        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

        self.name = name
