#!/usr/bin/python3
"""Basic tests for HBnB models"""

import unittest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class TestModels(unittest.TestCase):

    def test_user_creation(self):
        u = User("Ali", "Hassan", "ali@example.com")
        self.assertIsNotNone(u.id)
        self.assertEqual(u.first_name, "Ali")
        self.assertFalse(u.is_admin)

    def test_user_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Ali", "Hassan", "not-an-email")

    def test_amenity_creation(self):
        a = Amenity("Wi-Fi")
        self.assertEqual(a.name, "Wi-Fi")

    def test_place_and_relationships(self):
        owner = User("Owner", "One", "owner@example.com")
        p = Place("Nice place", owner, price=100.0, latitude=10, longitude=20)
        self.assertEqual(p.owner, owner)
        self.assertEqual(len(p.reviews), 0)
        self.assertEqual(len(p.amenities), 0)

        amenity = Amenity("Parking")
        p.add_amenity(amenity)
        self.assertEqual(len(p.amenities), 1)

    def test_review_creation(self):
        owner = User("Owner", "Two", "owner2@example.com")
        p = Place("Another place", owner)
        reviewer = User("Reviewer", "One", "reviewer@example.com")
        r = Review(p, reviewer, "Great!", 5)
        self.assertEqual(r.rating, 5)
        self.assertEqual(r.place, p)
        self.assertEqual(r.user, reviewer)


if __name__ == "__main__":
    unittest.main()

