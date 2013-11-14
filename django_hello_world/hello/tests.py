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
        self.client.get(reverse('home'))
        response = self.client.get(reverse('latest_requests'))
        latest_request = Request.objects.get(pk=1)
        self.assertContains(response, 'back')
        self.assertContains(response, latest_request)
