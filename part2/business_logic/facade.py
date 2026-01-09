#!/usr/bin/env python3

from persistence.in_memory_repository import InMemoryRepository
from business_logic.user import User
from business_logic.amenity import Amenity
from business_logic.place import Place
from business_logic.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------- USERS ----------
    def create_user(self, **data):
        user = User(**data)
        self.user_repo.add(user)
        return user

    def list_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, **data):
        user = self.get_user(user_id)
        if not user:
            return None
        allowed = ["first_name", "last_name", "email", "password"]
        filtered = {k: v for k, v in data.items() if k in allowed}
        user.update(**filtered)
        return user

    # ---------- AMENITIES ----------
    def create_amenity(self, **data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def list_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, **data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        allowed = ["name"]
        filtered = {k: v for k, v in data.items() if k in allowed}
        amenity.update(**filtered)
        return amenity

    # ---------- PLACES ----------
    def create_place(self, **data):
        place = Place(**data)
        self.place_repo.add(place)
        return place

    def list_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, **data):
        place = self.get_place(place_id)
        if not place:
            return None
        allowed = [
            "name",
            "description",
            "price",
            "latitude",
            "longitude",
            "amenity_ids"
        ]
        filtered = {k: v for k, v in data.items() if k in allowed}
        place.update(**filtered)
        return place

    # ---------- REVIEWS ----------
    def create_review(self, **data):
        review = Review(**data)
        self.review_repo.add(review)
        return review

    def list_reviews(self):
        return self.review_repo.get_all()

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, **data):
        review = self.get_review(review_id)
        if not review:
            return None
        allowed = ["text", "rating"]
        filtered = {k: v for k, v in data.items() if k in allowed}
        review.update(**filtered)
        return review

    def list_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return [
            r for r in self.review_repo.get_all()
            if r.place_id == place_id
        ]


facade = HBnBFacade()

