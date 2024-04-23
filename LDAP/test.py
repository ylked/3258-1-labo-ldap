import unittest
from flask_testing import TestCase
from app import app
import base64

users = (
    ('alice', 'alice', 'Alice Merveille'),
    ('bob', 'bob', 'Robert Dupont'),
    ('charlie', 'charlie', 'Charles Leroi')
)


class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def make_get_request_with_auth(self, username, password):
        cred = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {cred}'
        }

        return self.client.get('/fullname', headers=headers)

    def test_users_with_correct_credentials(self):
        for username, password, fullname in users:
            r = self.make_get_request_with_auth(username, password)
            self.assert200(r)
            self.assertEqual(r.data.decode('utf-8'), fullname)

    def test_not_giving_auth(self):
        r = self.client.get('/fullname')
        self.assert400(r)

    def test_giving_incorrect_passwords(self):
        for username, password, fullname in users:
            r = self.make_get_request_with_auth(username, password + '-')
            self.assert401(r)

    def test_giving_incorrect_usernames(self):
        r = self.make_get_request_with_auth('alsdfjapoisdfjqwe=cn&', 'asdf')
        self.assert401(r)


if __name__ == '__main__':
    unittest.main()
