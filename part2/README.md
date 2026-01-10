
# HBnB – Business Logic and API (Part 2)

## 📌 Project Overview

This project is **Part 2 of the HBnB application**, developed as part of the Holberton School curriculum.  
The goal of this part is to implement the **Business Logic layer** and the **RESTful API layer** based on the previously designed architecture.

## 📁 Project Structure

The project follows a modular and layered architecture to ensure clean code organization and separation of concerns.


|-- README.md
|-- TESTING.md
|-- api
|   |-- __init__.py
|   `-- v1
|       |-- __init__.py
|       |-- amenities.py
|       |-- places.py
|       |-- reviews.py
|       `-- users.py
|-- app.py
|-- business_logic
|   |-- __init__.py
|   |-- amenity.py
|   |-- base_model.py
|   |-- facade.py
|   |-- place.py
|   |-- review.py
|   `-- user.py
|-- persistence
|   |-- __init__.py
|   |-- in_memory_repository.py
|   `-- repository.py
|-- requirements.txt
`-- tests
    `-- __init__.py



The application provides core functionality for managing:
- Users
- Places
- Reviews
- Amenities

This part focuses on building a **clean, modular, and scalable backend foundation** using Python and Flask, without authentication or role-based access control, which will be handled in later parts.

---

## 🏗️ Architecture

The project follows a **layered architecture** with clear separation of concerns:

- **Presentation Layer**  
  Implemented using Flask and Flask-RESTx, responsible for handling API requests and responses.

- **Business Logic Layer**  
  Contains core domain models and application logic, managing relationships between entities.

- **Persistence Layer**  
  Uses an in-memory repository to temporarily store application data during runtime.

The **Facade design pattern** is used to simplify communication between the API layer and the business logic layer.


## 🛠️ Technologies Used

- Python 3
- Flask
- Flask-RESTx
- In-memory data storage
- RESTful API principles

## 📡 API Overview

The API provides CRUD operations for the following resources:

* **Users**
* **Places**
* **Reviews**
* **Amenities**

Each resource supports standard RESTful endpoints using JSON for request and response bodies.

---

## ✅ Testing and Validation

All API endpoints were tested using **black-box testing** via terminal tools such as `cURL`.
Both successful use cases and edge cases (invalid input, missing fields, invalid IDs) were validated to ensure the API behaves as expected and returns appropriate HTTP status codes.


## 👥 Team Members

* **Ali Abdullah Summan**
* **Ali Hassan Almaghrabi**
* **Omar Hail Alanzi**


## 📌 Notes

* This part of the project uses **in-memory persistence**, meaning data is reset when the application restarts.
* Authentication and authorization are intentionally not included and will be implemented in future parts.





