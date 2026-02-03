#!/usr/bin/python3
"""Review model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Represents a review made by a user on a place"""

    def __init__(self, place, user, text, rating):
        super().__init__()
        self.place = place
        self.user = user
        self.text = text
        self.rating = rating

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise ValueError("place must be a Place instance")
        self._place = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("user must be a User instance")
        self._user = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        # التعديل هنا: نستخدم value وليس text
        if not value or not isinstance(value, str):
            raise ValueError("text must be a non-empty string")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self._rating = value
