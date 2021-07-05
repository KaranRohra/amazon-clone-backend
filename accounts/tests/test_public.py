from django.test import TestCase

from accounts import models
from accounts import public
from accounts.tests import helper
from common.tests import helper as common_helper


class GetAddressByPkTestCase(TestCase):
    def setUp(self):
        self.user_object = helper.User()

    def test_get_address_with_valid_pk(self):
        expected_address = common_helper.create_address(user=self.user_object.user_1)[0]
        response = public.get_address_by_pk(1)
        self.assertEqual(expected_address, response)

    def test_get_address_with_invalid_pk(self):
        with self.assertRaises(models.Address.DoesNotExist):
            public.get_address_by_pk(1)
