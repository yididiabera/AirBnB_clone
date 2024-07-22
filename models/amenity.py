#!/usr/bin/python3
"""
This module defines the Amenity class, a representation of an amenity.

The Amenity class inherits from the BaseModel, providing basic model functionality.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity.

    Attributes:
        name (str): The name of the amenity.
    """

    name = ""
