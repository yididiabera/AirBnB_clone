#!/usr/bin/python3
"""
This module defines the City class, representing a city.

The City class inherits from the BaseModel, providing basic model functionality.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    Represents a city.

    Attributes:
        state_id (str): The ID of the state the city belongs to.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""
