from django.test import TestCase

from accounts import models
from accounts import public
from accounts.tests import helper


class GetAddressByPkTestCase(TestCase):
    def setUp(self):
        self.user_object = helper.User()

    def test_get_address_with_valid_pk(self):
        response = public.get_address_by_pk(1)
        self.assertEqual(self.user_object.user_1_address[0], response)

    def test_get_address_with_invalid_pk(self):
        with self.assertRaises(models.Address.DoesNotExist):
            public.get_address_by_pk(-1)
