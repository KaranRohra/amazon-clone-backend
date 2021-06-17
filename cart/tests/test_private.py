from django.test import TestCase

from common.tests import helper
from common.tests import constants
from cart import _private
from products import serializers


class GetProductTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD
        }
