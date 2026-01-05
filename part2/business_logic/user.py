#!/usr/bin/env python3
"""
User model for HBnB project.
"""

from business_logic.base_model import BaseModel


class User(BaseModel):
    """User class"""

    def __init__(self, first_name, last_name, email, password, **kwargs):
        """
        Initialize a new User instance.
        """
        super().__init__(**kwargs)

        if not first_name or not last_name:
            raise ValueError("first_name and last_name are required")

        if not email:
            raise ValueError("email is required")

        if not password:
            raise ValueError("password is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
