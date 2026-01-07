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
        user.update(**data)
        return user

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
        amenity.update(**data)
        return amenity

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
        place.update(**data)
        return place

    def create_review(self, **data):
        review = Review(**data)
        self.review_repo.add(review)
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
