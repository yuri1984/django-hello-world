"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Owner
from request.models import Request


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HelloTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_username = 'admin'
        self.test_password = 'admin'

    def test_home(self):
        """App renders proper template and database data"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assignment')
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Last name')
        self.assertContains(response, 'Date of birth')
        # Fixtures are rendered in the template/view
        owner = Owner.objects.get(pk=1)
        self.assertContains(response, owner.first_name)
        self.assertContains(response, owner.skype)
        self.assertContains(response, owner.jabber)

    def test_requests(self):
        for i in range(11):
            self.client.get(reverse('home'))
        response = self.client.get(reverse('latest_requests'))
        latest_request = Request.objects.get(pk=11)
        wrong_request = Request.objects.get(pk=1)
        self.assertContains(response, 'back')
        self.assertContains(response, latest_request)
        self.assertNotContains(response, wrong_request)

    def test_context_processor(self):
        response = self.client.get(reverse('home'))
        cp_in = False
        for d in response.context[0]:
            if 'django_settings' in d:
                cp_in = True
                break
        if not cp_in:
            raise AssertionError('django_settings context processor is not present in context')

    def test_login(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'login')
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'login')
        self.assertContains(response, 'Edit')

    def test_edit_page(self):
        changed_skype = 'fancy_skype_username'
        self.client.login(username=self.test_username, password=self.test_password)
        # we should have at leaset 1 Owner in fixtures
        owner = Owner.objects.filter()[0]
        user_input = owner.__dict__.copy()
        user_input['skype'] = changed_skype
        response = self.client.post(reverse('edit_home'), user_input)
        self.assertContains(response, changed_skype)
        response = self.client.get(reverse('home'))
        self.assertContains(response, changed_skype)

