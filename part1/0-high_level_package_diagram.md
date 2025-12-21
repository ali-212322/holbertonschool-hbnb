# 0. High-Level Package Diagram

This document presents the high-level architecture of the HBnB Evolution project.  
It illustrates the three main layers of the application (Presentation, Business Logic, and Persistence) and explains how they interact using the Facade Pattern.

---

## Architecture Overview

The HBnB application uses a 3-layer architecture:

- **Presentation Layer**: Handles communication with the user through API endpoints and services.
- **Business Logic Layer**: Contains the application's core logic and domain models.
- **Persistence Layer**: Manages data access, storage, and retrieval tasks.

Communication is performed using the **Facade Pattern**, which ensures controlled and simplified access between layers.

---

## High-Level Package Diagram

```mermaid
classDiagram
class PresentationLayer {
    <<Layer>>
    +API Endpoints
    +Services
}

class BusinessLogicLayer {
    <<Layer>>
    +Domain Models
    +Business Rules
}

class PersistenceLayer {
    <<Layer>>
    +Database Repositories
}

PresentationLayer --> BusinessLogicLayer : Facade Access
BusinessLogicLayer --> PersistenceLayer : CRUD Operations

