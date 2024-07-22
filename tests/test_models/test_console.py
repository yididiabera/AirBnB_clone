#!/usr/bin/python3
"""Unit tests for the HBNB command interpreter."""
import os
import uuid
import unittest
import models
from io import StringIO
from unittest.mock import patch
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for the HBNB command interpreter."""

    @classmethod
    def setUpClass(test_cls):
        """
        Set up the class for testing by renaming the existing JSON file if it exists.

        This method is called before any tests in this class are run.
        """
        try:
            os.rename("file.json", "tmp_file")
        except IOError:
            pass
        test_cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(test_cls):
        """
        Tear down the class by restoring the JSON file and closing the database session if needed.

        This method is called after all tests in this class have run.
        """
        try:
            os.rename("tmp_file", "file.json")
        except IOError:
            pass
        del test_cls.HBNB
        if isinstance(models.storage, DBStorage):
            models.storage._DBStorage__session.close()

    def setUp(self):
        """
        Set up the test environment by clearing the FileStorage objects dictionary.

        This method is called before each individual test.
        """
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """
        Clean up after tests by removing the JSON file if it exists.

        This method is called after each individual test.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass

    @unittest.skipIf(isinstance(models.storage, DBStorage), "Testing with FileStorage")
    def test_create(self):
        """
        Test the 'create' command of the HBNBCommand class.

        This test ensures that objects of various classes can be created.
        """
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create BaseModel")
            new_bm = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create State")
            new_state = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create User")
            new_user = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create City")
            new_city = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create Place")
            new_place = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create Review")
            new_review = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("create Amenity")
            new_amenity = test.getvalue().strip()

    @unittest.skipIf(isinstance(models.storage, DBStorage), "Testing with FileStorage")
    def test_all(self):
        """
        Test the 'all' command of the HBNBCommand class.

        This test ensures that objects of various classes can be listed.
        """
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all BaseModel")
            new_bm = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all State")
            new_state = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all User")
            new_user = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all City")
            new_city = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all Place")
            new_place = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all Review")
            new_review = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all Amenity")
            new_amenity = test.getvalue().strip()

    @unittest.skipIf(isinstance(models.storage, DBStorage), "Testing with FileStorage")
    def test_create_kwargs(self):
        """
        Test the 'create' command with keyword arguments.

        This test ensures that attributes can be set during the creation of a User object.
        """
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd('create User first_name="John" email="john@example.com" password="1234"')
            new_user = test.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as test:
            self.HBNB.onecmd("all User")
            user_output = test.getvalue()
            self.assertIn(new_user, user_output)
            self.assertIn("'first_name': 'John'", user_output)
            self.assertIn("'email': 'john@example.com'", user_output)
            self.assertNotIn("'last_name': 'Snow'", user_output)
            self.assertIn("'password': '1234'", user_output)


if __name__ == '__main__':
    unittest.main()

