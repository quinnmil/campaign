from django.test import TestCase

# Create your tests here.
from .models import Worker


class WorkerTest(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.email = 'email@address.com'
        self.first_name = 'firstname'
        self.last_name = 'lastname'

    def test_can_create_worker(self):

        new_user, new_worker = Worker.create(
            username=self.username,
            password=self.password,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.assertTrue(new_user.is_worker)
        self.assertEqual(new_worker.pay_earned, 0)
