#!/usr/bin/python3
""" Test Partner for expected behavior. """
import unittest
from models.base_model import BaseModel
from models.partner import Partner


class Test_Partner(unittest.TestCase):
    """ Test the Partner class"""
    def test_is_subclass(self):
        """ Test that Partner is a subclass of BaseModel. """
        partner = Partner()
        self.assertIsInstance(partner, BaseModel)
        self.assertTrue(hasattr(partner, "id"))
        self.assertTrue(hasattr(partner, "created_at"))
        self.assertTrue(hasattr(partner, "updated_at"))

    def test_email_attr(self):
        """ Test that Partner has attr email, and it's an empty string. """
        partner = Partner()
        self.assertTrue(hasattr(partner, "email"))
        self.assertEqual(partner.email, None)

    def test_username_attr(self):
        """Test that partner has attr username, and it's an empty string. """
        partner = Partner()
        self.assertTrue(hasattr(partner, "username"))
        self.assertEqual(partner.username, None)

    def test_to_dict_creates_dict(self):
        """ Test to_dict method creates a dictionary with proper attrs. """
        u = Partner()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """ Test that values in dict returned from to_dict are correct. """
        t_format = "%Y-%b-%d %H:%M"
        u = Partner()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "partner")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """ Test that the str method has the correct output. """
        partner = Partner()
        string = "[Partner] ({}) {}".format(partner.id, partner.__dict__)
        self.assertEqual(string, str(partner))
