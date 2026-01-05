#!/usr/bin/env python3
"""
Place model for HBnB project.
"""

from business_logic.base_model import BaseModel


class Place(BaseModel):
    """Place class"""

    def __init__(
        self,
        name,
        owner_id,
        description="",
        price=0.0,
        latitude=None,
        longitude=None,
        amenities=None,
        **kwargs
    ):
        """
        Initialize a new Place instance.
        """
        super().__init__(**kwargs)

        if not name:
            raise ValueError("Place name is required")

        if not owner_id:
            raise ValueError("owner_id is required")

        if price < 0:
            raise ValueError("price must be >= 0")

        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")

        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")

        self.name = name
        self.owner_id = owner_id
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = amenities if amenities is not None else []

