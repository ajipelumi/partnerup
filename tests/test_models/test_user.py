#!/usr/bin/python3
""" Test User for expected behavior. """
import unittest
from models.base_model import BaseModel
from models.user import User


class TestUser(unittest.TestCase):
    """ Test the User class"""
    def test_is_subclass(self):
        """ Test that User is a subclass of BaseModel. """
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """ Test that User has attr email, and it's an empty string. """
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, None)

    def test_password_attr(self):
        """ Test that User has attr password, and it's an empty string. """
        user = User()
        self.assertTrue(hasattr(user, "password"))
        self.assertEqual(user.password, None)

    def test_username_attr(self):
        """Test that User has attr username, and it's an empty string. """
        user = User()
        self.assertTrue(hasattr(user, "username"))
        self.assertEqual(user.username, None)

    def test_cohort_number_attr(self):
        """
        Test that User has attr cohort_number, and it's an empty string.
        """
        user = User()
        self.assertTrue(hasattr(user, "cohort_number"))
        self.assertEqual(user.cohort_number, None)

    def test_to_dict_creates_dict(self):
        """ Test to_dict method creates a dictionary with proper attrs. """
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """ Test that values in dict returned from to_dict are correct. """
        t_format = "%Y-%b-%d %H:%M"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """ Test that the str method has the correct output. """
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))


if __name__ == '__main__':
    unittest.main()
