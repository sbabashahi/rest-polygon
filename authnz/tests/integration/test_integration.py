import json

from django.test import TestCase, Client
from django.urls import reverse

from authnz.models import Profile


client = Client()

user_data = {"email": "saeed@gmail.com", "password": "saeed678"}


class AuthhnzTest(TestCase):

    def test_register_login(self):
        resp = client.post(reverse('register_email'), data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        resp = client.post(reverse('login_email'), data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        token = resp.json()['data']['token']
        header = {'HTTP_AUTHORIZATION': 'JWT {}'.format(token)}
        resp = client.get(reverse('refresh_token'), **header)
        self.assertEqual(resp.status_code, 200)


class UpdateProfile(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        resp = client.post(reverse('register_email'), data=json.dumps(user_data), content_type='application/json')

        resp = client.post(reverse('login_email'), data=json.dumps(user_data), content_type='application/json')

        token = resp.json()['data']['token']
        cls.header = {'HTTP_AUTHORIZATION': 'JWT {}'.format(token)}

    def test_name(self):
        resp = client.patch(reverse('update_profile'), data=json.dumps({'name': 'mamad'}),
                            content_type='application/json', **self.header)
        self.assertEqual(resp.status_code, 200)

        user = Profile.objects.get(user__username=user_data['email'])
        self.assertEqual(user.name, 'mamad')
        self.assertEqual(user.__str__(), user_data['email'])
