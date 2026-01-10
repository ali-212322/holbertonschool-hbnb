# Testing and Validation Report – HBnB Part 2

## Tools Used
- cURL
- Swagger UI (Flask-RESTx)
- unittest (basic automated tests)

## Testing Approach
Black-box testing was performed on all API endpoints using cURL and Swagger UI.  
Basic validation is handled through Flask-RESTx Swagger models and additional manual validation where required.  
Edge cases such as missing fields and invalid resource IDs were tested.

---

## Users Endpoint Testing

**POST /users**
- ✔ Valid input returns 201 Created
- ❌ Missing required fields returns 400 Bad Request (Swagger validation)

**GET /users**
- ✔ Returns list of users with status 200

**GET /users/{id}**
- ✔ Valid ID returns user data
- ❌ Invalid ID returns 404 User not found

**PUT /users/{id}**
- ✔ Valid update returns 200
- ❌ Invalid ID returns 404
- ⚠ Although partial updates are supported in logic, all fields are required by Swagger model

---

## Places Endpoint Testing

**POST /places**
- ✔ Valid input returns 201 Created
- ❌ Missing required fields returns 400 Bad Request (Swagger validation)
- ❌ Negative price returns 400 Bad Request
- ❌ Invalid owner_id returns 404 Not Found

**GET /places**
- ✔ Returns list of places with status 200
- ✔ Each place includes related reviews

**GET /places/{id}**
- ✔ Valid ID returns place data
- ❌ Invalid ID returns 404 Place not found

**PUT /places/{id}**
- ✔ Valid update returns 200
- ❌ Invalid ID returns 404
- ⚠ All fields are required by Swagger model despite partial update logic

---

## Reviews Endpoint Testing

**POST /reviews**
- ✔ Valid input returns 201 Created
- ❌ Missing required fields returns 400 Bad Request (Swagger validation)
- ❌ Invalid user_id or place_id returns 400 Bad Request

**GET /reviews**
- ✔ Returns list of reviews with status 200

**GET /reviews/{id}**
- ✔ Valid ID returns review data
- ❌ Invalid ID returns 404 Review not found

**PUT /reviews/{id}**
- ✔ Valid update returns 200
- ❌ Missing fields returns 400
- ❌ Invalid ID returns 404

**DELETE /reviews/{id}**
- ✔ Review deleted successfully

---

## Amenities Endpoint Testing

**POST /amenities**
- ✔ Valid input returns 201 Created
- ❌ Missing name returns 400 Bad Request

**GET /amenities**
- ✔ Returns list of amenities with status 200

**GET /amenities/{id}**
- ✔ Valid ID returns amenity data
- ❌ Invalid ID returns 404 Amenity not found

**PUT /amenities/{id}**
- ✔ Valid update returns 200
- ❌ Invalid ID returns 404

---

## Conclusion
All API endpoints were successfully tested using both manual and automated methods.  
Validation rules were correctly enforced through Swagger models and additional business logic checks.  
The API consistently returned appropriate HTTP status codes and handled edge cases as expected.

