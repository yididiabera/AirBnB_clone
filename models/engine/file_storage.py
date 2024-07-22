#!/usr/bin/python3
"""Module for the FileStorage class."""

import datetime
import json
import os


class FileStorage:
    """
    Class for managing the storage and retrieval of data.

    Attributes:
        __file_path (str): The file path where the JSON data is stored.
        __objects (dict): A dictionary storing all objects, keyed by their class name and ID.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary of stored objects.

        Returns:
            dict: The dictionary containing all stored objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the storage.

        Args:
            obj (BaseModel): The object to store, which must have an 'id' attribute.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes the dictionary of objects to a JSON file at the path specified by __file_path.
        """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            # Convert objects to dictionaries for serialization
            d = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(d, f)

    def classes(self):
        """
        Returns a dictionary of valid class names and their corresponding class references.

        Returns:
            dict: A dictionary where the keys are class names and the values are class references.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        return classes

    def reload(self):
        """
        Reloads objects from the JSON file into the storage.

        If the JSON file does not exist, this method does nothing. Otherwise, it reads the file,
        reconstructs objects from the data, and updates the storage dictionary.
        """
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            # Recreate objects from the dictionary
            obj_dict = {k: self.classes()[v["__class__"]](**v) for k, v in obj_dict.items()}
            # TODO: Determine whether this should overwrite or merge existing objects
            FileStorage.__objects = obj_dict

    def attributes(self):
        """
        Returns a dictionary of valid attributes and their types for each class.

        Returns:
            dict: A dictionary where the keys are class names and the values are dictionaries
                  mapping attribute names to their types.
        """
        attributes = {
            "BaseModel": {
                "id": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime
            },
            "User": {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str
            },
            "State": {
                "name": str
            },
            "City": {
                "state_id": str,
                "name": str
            },
            "Amenity": {
                "name": str
            },
            "Place": {
                "city_id": str,
                "user_id": str,
                "name": str,
                "description": str,
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "price_by_night": int,
                "latitude": float,
                "longitude": float,
                "amenity_ids": list
            },
            "Review": {
                "place_id": str,
                "user_id": str,
                "text": str
            }
        }
        return attributes
