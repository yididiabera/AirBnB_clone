#!/usr/bin/python3
"""
This module defines the Review class, representing a review.

The Review class inherits from the BaseModel, providing basic model functionality.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review.

    Attributes:
        place_id (str): The ID of the place being reviewed.
        user_id (str): The ID of the user who wrote the review.
        text (str): The text content of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
