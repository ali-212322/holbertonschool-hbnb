# 2. Sequence Diagrams for API Calls

This document presents detailed sequence diagrams for four critical API operations in the HBnB Evolution application. Each diagram illustrates the complete flow of interactions between the Presentation Layer, Business Logic Layer, and Persistence Layer.

---

## Overview

The sequence diagrams demonstrate how the system handles requests through the three-layer architecture using the Facade Pattern. Each diagram shows:
- Request initiation from the client
- Validation and processing in the Business Logic
- Data persistence operations
- Response flow back to the client

---

## 1. User Registration

**Use Case**: A new user signs up for an account in the HBnB application.

**Flow Description**:
1. User submits registration data (first_name, last_name, email, password)
2. API receives the request and forwards it to the Facade
3. Business Logic validates the data and checks for duplicate emails
4. If valid, user data is hashed (password) and saved to the database
5. Success response is returned with the new user's information

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(API)
    participant Facade as Business Logic<br/>(Facade)
    participant UserModel as Business Logic<br/>(User Model)
    participant DB as Persistence Layer<br/>(Database)

    Client->>API: POST /api/users/register<br/>{first_name, last_name, email, password}
    API->>Facade: register_user(user_data)
    
    Facade->>UserModel: validate_user_data(user_data)
    UserModel-->>Facade: validation_result
    
    alt Invalid Data
        Facade-->>API: Error: Invalid data
        API-->>Client: 400 Bad Request
    else Valid Data
        Facade->>DB: check_email_exists(email)
        DB-->>Facade: email_exists
        
        alt Email Already Exists
            Facade-->>API: Error: Email already registered
            API-->>Client: 409 Conflict
        else Email Available
            Facade->>UserModel: create_user(user_data)
            UserModel->>UserModel: hash_password()
            UserModel->>UserModel: generate_id()
            UserModel->>UserModel: set_timestamps()
            
            UserModel->>DB: save(user_object)
            DB-->>UserModel: user_saved
            UserModel-->>Facade: user_created
            
            Facade-->>API: Success: User registered
            API-->>Client: 201 Created<br/>{user_id, email, created_at}
        end
    end
```

**Key Points**:
- Email uniqueness is validated before creating the user
- Password is hashed for security before storage
- UUID is automatically generated for the user
- Timestamps (created_at, updated_at) are set automatically

---

## 2. Place Creation

**Use Case**: A registered user creates a new place listing.

**Flow Description**:
1. User submits place details (title, description, price, location, amenities)
2. API authenticates the user and validates ownership rights
3. Business Logic validates place data and coordinates
4. Place is created and associated with the owner
5. Selected amenities are linked to the place

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(API)
    participant Facade as Business Logic<br/>(Facade)
    participant PlaceModel as Business Logic<br/>(Place Model)
    participant AmenityModel as Business Logic<br/>(Amenity Model)
    participant DB as Persistence Layer<br/>(Database)

    Client->>API: POST /api/places<br/>{title, description, price, lat, long, amenities[]}
    API->>API: authenticate_user()
    
    alt Authentication Failed
        API-->>Client: 401 Unauthorized
    else Authenticated
        API->>Facade: create_place(place_data, owner_id)
        
        Facade->>PlaceModel: validate_place_data(place_data)
        PlaceModel->>PlaceModel: validate_coordinates(lat, long)
        PlaceModel->>PlaceModel: validate_price(price)
        PlaceModel-->>Facade: validation_result
        
        alt Invalid Data
            Facade-->>API: Error: Invalid place data
            API-->>Client: 400 Bad Request
        else Valid Data
            Facade->>PlaceModel: create_place(place_data)
            PlaceModel->>PlaceModel: generate_id()
            PlaceModel->>PlaceModel: set_timestamps()
            PlaceModel->>PlaceModel: set_owner_id(owner_id)
            
            PlaceModel->>DB: save(place_object)
            DB-->>PlaceModel: place_saved
            
            loop For each amenity_id
                Facade->>AmenityModel: verify_amenity_exists(amenity_id)
                AmenityModel->>DB: get_amenity(amenity_id)
                DB-->>AmenityModel: amenity_data
                AmenityModel-->>Facade: amenity_valid
                
                Facade->>DB: link_place_amenity(place_id, amenity_id)
                DB-->>Facade: link_created
            end
            
            PlaceModel-->>Facade: place_created_with_amenities
            Facade-->>API: Success: Place created
            API-->>Client: 201 Created<br/>{place_id, title, owner_id, amenities[], created_at}
        end
    end
```

**Key Points**:
- User authentication is required before place creation
- Coordinates (latitude, longitude) are validated for proper ranges
- Price must be a positive value
- Amenities are verified to exist before linking
- Many-to-many relationship between Place and Amenity is established

---

## 3. Review Submission

**Use Case**: A user submits a review for a place they visited.

**Flow Description**:
1. User submits review data (rating, comment) for a specific place
2. API authenticates the user
3. Business Logic validates the review and checks if place exists
4. System prevents owner from reviewing their own place
5. Review is saved and linked to both user and place

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(API)
    participant Facade as Business Logic<br/>(Facade)
    participant ReviewModel as Business Logic<br/>(Review Model)
    participant PlaceModel as Business Logic<br/>(Place Model)
    participant DB as Persistence Layer<br/>(Database)

    Client->>API: POST /api/places/{place_id}/reviews<br/>{rating, comment}
    API->>API: authenticate_user()
    
    alt Authentication Failed
        API-->>Client: 401 Unauthorized
    else Authenticated
        API->>Facade: create_review(place_id, user_id, review_data)
        
        Facade->>PlaceModel: get_place(place_id)
        PlaceModel->>DB: fetch_place(place_id)
        DB-->>PlaceModel: place_data
        PlaceModel-->>Facade: place_object
        
        alt Place Not Found
            Facade-->>API: Error: Place not found
            API-->>Client: 404 Not Found
        else Place Exists
            Facade->>Facade: check_if_owner(user_id, place.owner_id)
            
            alt User is Owner
                Facade-->>API: Error: Cannot review own place
                API-->>Client: 403 Forbidden
            else User is Not Owner
                Facade->>ReviewModel: validate_review_data(review_data)
                ReviewModel->>ReviewModel: validate_rating(1-5)
                ReviewModel->>ReviewModel: validate_comment()
                ReviewModel-->>Facade: validation_result
                
                alt Invalid Data
                    Facade-->>API: Error: Invalid review data
                    API-->>Client: 400 Bad Request
                else Valid Data
                    Facade->>ReviewModel: create_review(review_data)
                    ReviewModel->>ReviewModel: generate_id()
                    ReviewModel->>ReviewModel: set_timestamps()
                    ReviewModel->>ReviewModel: set_user_id(user_id)
                    ReviewModel->>ReviewModel: set_place_id(place_id)
                    
                    ReviewModel->>DB: save(review_object)
                    DB-->>ReviewModel: review_saved
                    ReviewModel-->>Facade: review_created
                    
                    Facade-->>API: Success: Review submitted
                    API-->>Client: 201 Created<br/>{review_id, rating, place_id, user_id, created_at}
                end
            end
        end
    end
```

**Key Points**:
- User must be authenticated to submit a review
- Place existence is verified before creating review
- Business rule: Users cannot review their own places
- Rating must be between 1 and 5
- Each review is linked to both a user and a place

---

## 4. Fetching a List of Places

**Use Case**: A user requests a list of available places, optionally filtered by criteria.

**Flow Description**:
1. User requests places list with optional filters (location, price range, amenities)
2. API receives request with query parameters
3. Business Logic processes filters and builds query criteria
4. Database retrieves matching places with their associated amenities
5. Results are formatted and returned to the client

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(API)
    participant Facade as Business Logic<br/>(Facade)
    participant PlaceModel as Business Logic<br/>(Place Model)
    participant AmenityModel as Business Logic<br/>(Amenity Model)
    participant DB as Persistence Layer<br/>(Database)

    Client->>API: GET /api/places?filters={price_max, lat, long, amenities[]}
    API->>Facade: get_places(filters)
    
    Facade->>PlaceModel: validate_filters(filters)
    PlaceModel->>PlaceModel: validate_price_range()
    PlaceModel->>PlaceModel: validate_coordinates()
    PlaceModel-->>Facade: filters_valid
    
    alt Invalid Filters
        Facade-->>API: Error: Invalid filter parameters
        API-->>Client: 400 Bad Request
    else Valid Filters
        Facade->>PlaceModel: build_query(filters)
        PlaceModel-->>Facade: query_criteria
        
        Facade->>DB: fetch_places(query_criteria)
        DB-->>Facade: places_list
        
        alt No Places Found
            Facade-->>API: Empty list
            API-->>Client: 200 OK<br/>{places: [], count: 0}
        else Places Found
            loop For each place
                Facade->>DB: get_place_amenities(place_id)
                DB-->>Facade: amenities_list
                
                Facade->>PlaceModel: attach_amenities(place, amenities)
                PlaceModel-->>Facade: place_with_amenities
                
                Facade->>DB: get_owner_info(owner_id)
                DB-->>Facade: owner_data
                
                Facade->>PlaceModel: attach_owner(place, owner)
                PlaceModel-->>Facade: enriched_place
            end
            
            Facade->>Facade: sort_and_paginate(places)
            Facade-->>API: places_list_enriched
            API-->>Client: 200 OK<br/>{places: [...], count: n, page: 1}
        end
    end
```

**Key Points**:
- No authentication required for browsing places (public endpoint)
- Filters are validated before querying database
- Each place includes its associated amenities
- Owner information is included for each place
- Results can be sorted and paginated
- Empty results return successfully with count of 0

---

## Summary

These sequence diagrams demonstrate the complete flow of four critical operations in the HBnB Evolution application:

1. **User Registration**: Shows validation, email uniqueness check, and secure password handling
2. **Place Creation**: Demonstrates authentication, data validation, and amenity linking
3. **Review Submission**: Illustrates business rules enforcement (no self-reviews) and relationship management
4. **Fetching Places**: Shows query building, filtering, and data enrichment with related entities

Each diagram follows the three-layer architecture pattern with clear separation of concerns:
- **Presentation Layer**: Handles HTTP requests/responses and authentication
- **Business Logic Layer**: Validates data, enforces business rules, and orchestrates operations
- **Persistence Layer**: Manages data storage and retrieval

The Facade Pattern is consistently used to provide a clean interface between layers, ensuring maintainability and scalability of the application.

---

## Design Decisions

1. **Authentication Flow**: Placed at the API layer to catch unauthorized requests early
2. **Validation Strategy**: Two-level validation (format validation in Business Logic, existence checks in Persistence)
3. **Error Handling**: Clear error responses with appropriate HTTP status codes
4. **Data Enrichment**: Related data (amenities, owner info) is fetched and attached in the Business Logic layer
5. **Timestamps**: Automatically managed by the model layer for audit purposes

These diagrams serve as a blueprint for implementing the API endpoints and ensure consistent behavior across the application.
