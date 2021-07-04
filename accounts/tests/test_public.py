from django.test import TestCase

from accounts import public
from accounts import models
from common.tests import helper
from common.tests import constants


class GetAddressByPkTestCase(TestCase):
    def test_get_address_with_valid_pk(self):
        user = helper.create_user(**constants.USER_INFO)
        expected_address = helper.create_address(user=user)[0]
        response = public.get_address_by_pk(1)
        self.assertEqual(expected_address, response)
    
    def test_get_address_with_invalid_pk(self):
        with self.assertRaises(models.Address.DoesNotExist): 
            public.get_address_by_pk(1)
