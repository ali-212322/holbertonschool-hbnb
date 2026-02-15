# 🏠 HBnB Project

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-REST%20API-black)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
**HBnB** is a simplified Airbnb-like full-stack web application developed as part of the **Holberton School** curriculum.

The system allows users to:
- Register and login securely
- Create and manage places
- Add amenities (admin only)
- Write and manage reviews
- Interact through a simple web client (frontend)

This project was built in **4 phases**:
- **Part 1:** UML Design
- **Part 2:** REST API + Business Logic (In-Memory Repository)
- **Part 3:** Authentication + Database Persistence (JWT + SQLAlchemy)
- **Part 4:** Simple Web Client (HTML/CSS/JavaScript)

## 🎯 Features

### 👤 User Management
- Create and manage users
- Secure password hashing using **Bcrypt**
- Role-Based Access Control (**Admin vs User**)

### 🔐 Authentication
- JWT authentication system
- Protected API endpoints
- Admin authorization using JWT claims

### 🏡 Places
- Create and update places
- Public access to list and view place details
- Owner/Admin permissions for modifications

### ⭐ Reviews
- Add reviews with rating validation (1–5)
- Users cannot review their own places
- Users cannot review the same place twice
- Owner/Admin update and delete permissions

### 🛠️ Amenities
- Public listing of amenities
- Admin-only create/update/delete

### 🌐 Web Client (Frontend)
- Login page
- List places with price filter
- Place details page
- Add review page
- Uses **Fetch API** and JWT stored in cookies

## 🏗️ Architecture
The project follows a **Layered Architecture**:

- **Presentation Layer:** Flask-RESTX API endpoints (JSON I/O)
- **Business Logic Layer:** Business rules and validations via **Facade Pattern**
- **Persistence Layer:** SQLAlchemy ORM with **Repository Pattern**

This structure improves maintainability and scalability.

## 🧩 UML Design (Part 1)
The system was designed using UML diagrams:
- Class Diagram
- Package Diagram
- Sequence Diagrams

### Main Entities
- **User**
- **Place**
- **Review**
- **Amenity**

### Relationships
- User → Places (**One-to-Many**)
- User → Reviews (**One-to-Many**)
- Place → Reviews (**One-to-Many**)
- Place ↔ Amenity (**Many-to-Many**)

## ⚙️ Technologies Used

### Backend
- Python 3
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-CORS
- SQLAlchemy
- SQLite (development)

### Frontend
- HTML5
- CSS3
- JavaScript (ES6)
- Fetch API

### Tools
- Git & GitHub
- Swagger UI (API Documentation & Testing)

## 📁 Project Structure
```text
holbertonschool-hbnb/
│
├── part1/
│   └── UML diagrams
│
├── part2/
│   ├── app/
│   └── run.py
│
├── part3/
│   ├── app/
│   │   ├── api/v1/
│   │   ├── models/
│   │   ├── persistence/
│   │   ├── services/
│   │   ├── extensions.py
│   │   └── __init__.py
│   ├── config.py
│   └── run.py
│
└── part4/
    ├── login.html
    ├── index.html
    ├── place.html
    ├── add_review.html
    ├── styles.css
    └── scripts/
