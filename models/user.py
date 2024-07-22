#!/usr/bin/python3
"""
This module defines the User class, representing a user.

The User class inherits from the BaseModel, providing basic model functionality.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user.

    Attributes:
        email (str): The user's email address.
        password (str): The user's password.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
