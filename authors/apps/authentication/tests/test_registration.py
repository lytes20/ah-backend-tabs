from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import RegistrationAPIView
import json
from minimock import Mock
import smtplib


class RegisterUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }
        self.request = self.factory.post(
            '/api/users/', data=json.dumps(self.user), content_type='application/json')
        self.response = RegistrationAPIView.as_view()(self.request)
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

    def test_user_registration_success(self):

        self.assertEqual(self.response.status_code, 201)

    def test_user_registration_with_empty_credentials(self):

        user = {}
        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')

        response = RegistrationAPIView.as_view()(request)

        self.assertIn('This field is required.',
                      response.data["errors"]["email"][0])
        self.assertIn('This field is required.',
                      response.data["errors"]["username"][0])
        self.assertIn('This field is required.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_user_registration_with_invalid_email(self):
        """ Wrong email address without @ """

        user = {
            "user": {
                "email": "testgmail.com",
                "username": "tester",
                "password": "testpassword"
            }
        }

        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')

        response = RegistrationAPIView.as_view()(request)

        self.assertIn('Enter a valid email address.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_user_registration_for_email_that_already_exists(self):
        """ Use the same email that was used when setting up """

        request = self.factory.post(
            '/api/users/', data=json.dumps(self.user), content_type='application/json')

        response = RegistrationAPIView.as_view()(request)

        self.assertEqual("We cannot register you because there's a user with that email already.",
                         response.data["errors"]["email"][0])

        self.assertEqual(response.status_code, 400)

    def test_user_registration_for_username_that_already_exists(self):
        """ Use the same username that was used when setting up """

        request = self.factory.post(
            '/api/users/', data=json.dumps(self.user), content_type='application/json')

        response = RegistrationAPIView.as_view()(request)

        self.assertIn("We cannot register you because there's a user with that username already.",
                      response.data["errors"]["username"][0])
        self.assertEqual(response.status_code, 400)
