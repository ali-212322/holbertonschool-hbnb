#!/usr/bin/env python3
"""
Amenity model for HBnB project.
"""

from business_logic.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class"""

    def __init__(self, name, **kwargs):
        """
        Initialize a new Amenity instance.
        """
        super().__init__(**kwargs)

        if not name:
            raise ValueError("Amenity name is required")

        self.name = name
