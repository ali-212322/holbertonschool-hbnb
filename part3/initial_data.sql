-- تنظيف البيانات لضمان بداية نظيفة
DELETE FROM reviews;
DELETE FROM places;
DELETE FROM amenities;
DELETE FROM users;

-- 1. حقن المستخدمين (يوجد لديهم كلاس user.py)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES 
('u-admin', 'Ali', 'Abdullah', 'admin@hbnb.com', 'pass_admin', 1),
('u-host-1', 'Sami', 'Khalid', 'sami@host.com', 'pass_host', 0),
('u-guest-1', 'Sara', 'Ahmed', 'sara@guest.com', 'pass_guest', 0);

-- 2. حقن المرافق (يوجد لديهم كلاس amenity.py)
INSERT INTO amenities (id, name) VALUES 
('a1', 'WiFi'), 
('a2', 'Swimming Pool'), 
('a3', 'Air Conditioning');

-- 3. حقن أماكن (يوجد لديهم كلاس place.py)
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES 
('p1', 'Modern Apartment', 'Near city center', 120.00, 24.71, 46.67, 'u-host-1'),
('p2', 'Desert Resort', 'Quiet and peaceful', 350.00, 24.85, 46.50, 'u-host-1');

-- 4. حقن تقييمات (يوجد لديهم كلاس review.py)
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES 
('r1', 'Clean and tidy!', 5, 'u-guest-1', 'p1'),
('r2', 'A bit far from shops', 3, 'u-guest-1', 'p2');
