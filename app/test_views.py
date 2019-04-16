from unittest import TestCase

from django.test import Client
import pytest


# Create your tests here.

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_correct_landing_page_response(self):
        # Get login page
        response = self.client.get('/')

        # Check response code
        self.assertEquals(response.status_code, 200)
