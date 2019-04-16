import unittest

from django.contrib.auth.models import User
from django.test import Client
from parameterized import parameterized_class, parameterized

from app.models import Institution, Gift


class LandingPageTestCase(unittest.TestCase):

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
        self.assertEquals(response.url, '/#contact')

    def tearDown(self):
        Institution.objects.all().delete()
        Gift.objects.all().delete()


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='TestUser', email='test@test.com', password='testpassword')

    def test_correct_login(self):
        # Check response code for login user
        self.client.login(username='TestUser', password='testpassword')
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        # check corect user name in response context

        self.assertEquals(response.context['user'].username, 'TestUser')

        # check if user is not anonymous
        self.assertFalse(self.user.is_anonymous)

        # check logout
        response = self.client.get('/logout/')
        self.assertIsNone(response.context)

    @parameterized.expand([{"username": "TestUser2",
                            "password": "testpassword"
                            },
                           {"username": "TestUser",
                            "password": "testpassword2"
                            }])
    def test_incorrect_login(self, username, password):
        # Check incorect data for user
        self.client.login(username=username, password=password)
        response = self.client.get('/accounts/login/')
        self.assertNotEquals(response.context['user'].username, 'Testowy2')

    def tearDown(self):
        User.objects.all().delete()


if __name__ == '__main__':
    unittest.main()
