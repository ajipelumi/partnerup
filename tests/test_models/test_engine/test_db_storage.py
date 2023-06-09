import unittest
import models
from models.user import User
from models.partner import Partner


class TestDBStorage(unittest.TestCase):
    def test_get(self):
        """ Tests method for getting an instance. """
        dic = {
            "username": "Pelumi",
            "password": "pelumi_pwd",
            "email": "pelumi@partnerup.com",
            "cohort_number": 14
            }
        instance = User(**dic)
        models.storage.new(instance)
        models.storage.save()
        get_instance = models.storage.get(User, instance.id)
        self.assertEqual(get_instance, instance)

    def test_count(self):
        """ Tests count method. """
        dic = {
            "username": "Ahmad",
            "password": "ahmad_pwd",
            "email": "ahmad@partnerup.com",
            "cohort_number": 14
            }
        user = User(**dic)
        models.storage.new(user)
        dic = {
            "username": "Moussa",
            "email": "moussa@partnerup.com",
            "cohort_number": 14
            }
        partner = Partner(**dic)
        models.storage.new(partner)
        models.storage.save()
        c = models.storage.count()
        self.assertEqual(len(models.storage.all()), c)


if __name__ == '__main__':
    unittest.main()
