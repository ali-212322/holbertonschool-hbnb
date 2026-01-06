#!/usr/bin/env python3
"""
Facade: the ONLY entry point used by the API.
"""

from business_logic.user import User
from business_logic.place import Place
from business_logic.review import Review
from business_logic.amenity import Amenity
from persistence.in_memory_repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.users = InMemoryRepository()
        self.places = InMemoryRepository()
        self.reviews = InMemoryRepository()
        self.amenities = InMemoryRepository()

    # -------- USERS --------
    def create_user(self, first_name, last_name, email, password):
        user = User(first_name, last_name, email, password)
        self.users.add(user)
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def list_users(self):
        return self.users.get_all()

    def update_user(self, user_id, **data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(**data)
        return user

    # -------- PLACES --------
    def create_place(self, name, owner_id, **kwargs):
        if not self.get_user(owner_id):
            raise ValueError("Owner not found")

        place = Place(name=name, owner_id=owner_id, **kwargs)
        self.places.add(place)
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def list_places(self):
        return self.places.get_all()

    def update_place(self, place_id, **data):
        place = self.get_place(place_id)
        if not place:
            return None
        place.update(**data)
        return place

    # -------- REVIEWS (TASK 5) --------
    def create_review(self, text, user_id, place_id):
        if not self.get_user(user_id):
            raise ValueError("User not found")
        if not self.get_place(place_id):
            raise ValueError("Place not found")

        review = Review(text=text, user_id=user_id, place_id=place_id)
        self.reviews.add(review)
        return review

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def list_reviews(self):
        return self.reviews.get_all()

    def list_reviews_by_place(self, place_id):
        if not self.get_place(place_id):
            raise ValueError("Place not found")
        return [r for r in self.reviews.get_all() if r.place_id == place_id]

    def update_review(self, review_id, **data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(**data)
        return review

    def delete_review(self, review_id):
        return self.reviews.delete(review_id)


facade = HBnBFacade()
