#!/usr/bin/python3
"""Console TestCases """

import unittest
import sys
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        """Redirect stdout to capture console output for testing."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore normal stdout behavior."""
        self.held_output.close()
        sys.stdout = sys.__stdout__

    def test_create(self):
        console = HBNBCommand()

        # Test create command for BaseModel
        console.onecmd("create BaseModel name=\"Test Model\" number_rooms=3")
        captured_output = self.held_output.getvalue().strip()
        self.assertTrue(captured_output.startswith("[BaseModel]"))

        # Test create command for User
        console.onecmd("create User email=\"test@ele.com\" password=\"pwd\"")
        captured_output = self.held_output.getvalue().strip()
        self.assertTrue(captured_output.startswith("[User]"))

    def test_show(self):
        console = HBNBCommand()

        # Test show command for existing object
        console.onecmd("create BaseModel name=\"Test Model\"")
        console.onecmd("show BaseModel " + console.id)
        captured_output = self.held_output.getvalue().strip()
        self.assertTrue(captured_output.startswith("[BaseModel]"))

        # Test show command for non-existing object
        console.onecmd("show BaseModel non_existent_id")
        captured_output = self.held_output.getvalue().strip()
        self.assertEqual(captured_output, "** no instance found **")

    def test_destroy(self):
        console = HBNBCommand()

        # Test destroy command for existing object
        console.onecmd("create BaseModel name=\"Test Model\"")
        console.onecmd("destroy BaseModel " + console.id)
        captured_output = self.held_output.getvalue().strip()
        self.assertEqual(captured_output, "")

        # Test destroy command for non-existing object
        console.onecmd("destroy BaseModel non_existent_id")
        captured_output = self.held_output.getvalue().strip()
        self.assertEqual(captured_output, "** no instance found **")


if __name__ == '__main__':
    unittest.main()
