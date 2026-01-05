#!/usr/bin/env python3
"""
Base model for HBnB project.
Provides common attributes for all business logic classes.
"""

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models"""

    def __init__(self, **kwargs):
        """Initialize a new BaseModel instance."""
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def update(self, **kwargs):
        """Update attributes of the model."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return a dictionary representation of the model."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
