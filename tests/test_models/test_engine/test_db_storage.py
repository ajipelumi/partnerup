import unittest
from models import storage
from models.user import User
from models.partner import Partner


class Test_DBStorage(unittest.TestCase):
    def test_get(self):
        """ Tests method for getting an instance. """
        dic = {"username": "Pelumi"}
        instance = User(**dic)
        storage.new(instance)
        storage.save()
        get_instance = storage.get(User, instance.id)
        self.assertEqual(get_instance, instance)

    def test_count(self):
        """ Tests count method. """
        dic = {"username": "Ahmad"}
        user = User(**dic)
        storage.new(user)
        dic = {"username": "Moussa", "user_id": user.id}
        partner = Partner(**dic)
        storage.new(partner)
        storage.save()
        c = storage.count()
        self.assertEqual(len(storage.all()), c)


if __name__ == '__main__':
    unittest.main()
