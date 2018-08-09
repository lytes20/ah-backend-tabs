from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import LoginAPIView, RegistrationAPIView, VerificationAPIView
import json
from minimock import Mock
import smtplib


class LoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_to_login = {
            "user": {
                "email": "rutale@gmail.com",
                "password": "rutale1234*",
                "username": "rutale"
            }
        }

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.make_token(self.user_to_login)
        }
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')  

    def make_token(self, user):
        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')
        response = RegistrationAPIView.as_view()(request)
        verfication_request = self.factory.put(
            '/api/users/verify/token', data=json.dumps(user), content_type='application/json')
        VerificationAPIView.as_view()(verfication_request, **
                                      {"token": response.data["token"]})
        return response.data['token']

    def test_normal_login(self):
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(self.user_to_login), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_email(self):
        user = {
            'user': {
                'email': 'rut@gmail.com',
                'password': 'rutale1234*'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('A user with this email and password was not found.',
                      response.data["errors"]["error"][0])
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        user = {
            'user': {
                'email': 'rutale@gmail.com',
                'password': 'rutale123'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_login_missing_email(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': '',
                'password': 'rutale1234*'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field may not be blank.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_login_missing_password(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                'password': ''
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field may not be blank.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_email_index(self):
        user = {
            'user': {
                'username': 'rutale',
                '': 'rut@gmail.com',
                'password': 'rutale1234*'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_password_index(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                '': 'rutaleivan'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_password_field(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_email_field(self):
        user = {
            'user': {
                'username': 'rutale',
                'password': 'rutale1234*'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_username_field(self):
        user = {
            'user': {
                'email': 'rutale@gmail.com',
                'password': 'rutale1234*'
            }
        }
        request = self.factory.post(
            "/api/users/login", **self.headers, data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
