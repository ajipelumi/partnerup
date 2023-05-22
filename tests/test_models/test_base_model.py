#!/usr/bin/python3
""" Test BaseModel for expected behavior. """
from datetime import datetime
import time
import unittest
from unittest import mock
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """ Test the BaseModel class. """
    def test_instantiation(self):
        """ Test that object is correctly created. """
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "PartnerUp"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "PartnerUp")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """
        Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value.
        """
        inst1 = BaseModel()
        time.sleep(0.1)
        inst2 = BaseModel()
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """ Test that id is a valid uuid. """
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """ Test conversion of object attributes to dictionary for json. """
        my_model = BaseModel()
        my_model.name = "PartnerUp"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "PartnerUp")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """ Test that values in dict returned from to_dict are correct. """
        t_format = "%Y-%b-%d %H:%M"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """ Test that the str method has the correct output. """
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """
        Test that save method updates `updated_at` and calls
        save().
        """
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)


if __name__ == '__main__':
    unittest.main()
