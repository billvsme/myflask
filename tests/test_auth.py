# coding: utf-8
import unittest
from base64 import b64encode
from app import create_app, db
from app.models.users import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_headers(self, username, password):
        return {
            'Authorization': 'Bearer ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accpet': 'application/json',
            'Content=Type': 'application/json'
        }

    def test_login(self):
        # test login success
        u = User(email='hahaha@example.com', username='hahaha', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            '/auth/login',
            json={'email': 'hahaha@example.com', 'password': 'password'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue('access_token' in response.get_json())

        # test login error
        response = self.client.post(
            '/auth/login',
            json={'email': 'hahaha@example.com', 'password': 'errorpassword'}
        )

        self.assertEqual(response.status_code, 401)

    def test_register(self):
        # test register
        response = self.client.post(
            '/auth/register',
            json={'email': 'billvsme@163.com', 'password': 'password', 'username': 'hahaha'}
        )
        self.assertEqual(response.status_code, 200)

        u = User.query.filter_by(email='billvsme@163.com').first()
        self.assertTrue(u is not None)
        self.assertEqual(u.confirmed, False)

    def test_confirm(self):
        # test login success
        u = User(email='hahaha@example.com', username='hahaha', password='password')
        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            '/auth/login',
            json={'email': 'hahaha@example.com', 'password': 'password'}
        )

        self.assertFalse(u.confirmed)

        auth_token = response.get_json()['access_token']

        confirm_token = u.generate_confirmation_token()
        response = self.client.get(
            '/auth/confirm/{}'.format(confirm_token),
            headers=self.get_headers(auth_token, '')
        )
        db.session.refresh(u)

        self.assertTrue(u.confirmed)

    def test_change_password(self):
        u = User(email='hahaha@example.com', username='hahaha', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        auth_token = u.generate_auth_token()
        response = self.client.post(
            '/auth/change-password',
            headers=self.get_headers(auth_token, ''),
            json={'old_password': 'password', 'new_password': 'changed_password'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(u.verify_password('changed_password'))

    def test_reset_password(self):
        u = User(email='hahaha@example.com', username='hahaha', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            '/auth/reset-password',
            json={'email': 'hahaha@example.com'}
        )

        self.assertEqual(response.status_code, 200)
        reset_token = u.generate_reset_token()

        response = self.client.get(
            '/auth/reset-password/{}'.format(reset_token),
            json={'new_password': 'reset_password'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(u.verify_password('reset_password'))
