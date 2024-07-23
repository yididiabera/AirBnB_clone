#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    A base class for all hbnb models.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new model instance.

        Args:
            *args (tuple): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments to set instance attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def save(self):
        """
        Updates the public instance attribute 'updated_at' with the current datetime
        and calls the storage save method to persist the instance changes.
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance's __dict__.

        Returns:
            dict: Dictionary representation of the instance, including the class name
            and ISO-formatted datetime attributes.
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict

    def __str__(self):
        """
        Returns the string representation of the instance.

        Returns:
            str: String representation in the format [<class name>] (<self.id>) <self.__dict__>.
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)
