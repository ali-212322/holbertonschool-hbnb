#!/usr/bin/env python3
"""
Review model for HBnB project.
"""

from business_logic.base_model import BaseModel


class Review(BaseModel):
    """Review class"""

    def __init__(self, text, user_id, place_id, **kwargs):
        """
        Initialize a new Review instance.
        """
        super().__init__(**kwargs)

        if not text:
            raise ValueError("Review text is required")

        if not user_id:
            raise ValueError("user_id is required")

        if not place_id:
            raise ValueError("place_id is required")

        self.text = text
        self.user_id = user_id
        self.place_id = place_id
