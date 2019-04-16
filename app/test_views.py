import sys
import unittest

from django.test import Client
import sys

from app.models import Institution, Gift

print(sys.version)


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.institution = Institution.objects.create(name='Testowa', address='ul. Testowa Testowo')
        self.gift = Gift.objects.create()

    def test_landing_page_response(self):
        # Check response code
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_institution_ammount(self):
        # check number of intitution
        response = self.client.get('/')
        self.assertEquals(response.context['all_institutions_count'], 0)
        self.institution.approved = True
        self.institution.save()
        response = self.client.get('/')
        self.assertEquals(response.context['all_institutions_count'], 1)

    def test_gift_ammount(self):
        response = self.client.get('/')
        self.assertEquals(response.context['gifts'], 0)
        self.gift.given = True
        self.gift.save()
        response = self.client.get('/')
        self.assertEquals(response.context['gifts'], 1)

    def test_bags_ammount(self):
        response = self.client.get('/')
        self.assertEquals(response.context['bags'], 0)
        self.gift.given = True
        self.gift.clothes_to_use = 1
        self.gift.save()
        response = self.client.get('/')
        self.assertEquals(response.context['bags'], 1)

    def test_correct_landing_page(self):
        response = self.client.post('/')
        self.assertEquals(response.url, '/landing-page#contact')

    def tearDown(self):
        Institution.objects.all().delete()
        Gift.objects.all().delete()


if __name__ == '__main__':
    unittest.main()
