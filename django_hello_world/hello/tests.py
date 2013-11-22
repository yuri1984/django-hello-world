"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os
import cStringIO
import sys

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

from models import Owner
from models import ModelsLog
from request.models import Request


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
                if not hasattr(d['django_settings'], 'DATABASES'):
                    raise AssertionError('django.settings, provided by context processeor are not django settings')
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

    def test_edit_page_login(self):
        testfile = os.path.join(settings.FIXTURE_DIRS[0], 'testdata', 'tf1.png')
        changed_skype = 'fancy_skype_username'
        file_present_string = 'pictures/tf1'
        with open(testfile, 'r') as tf:
            self.client.login(username=self.test_username, password=self.test_password)
            # we should have at leaset 1 Owner in fixtures
            owner = Owner.objects.filter()[0]
            user_input = owner.__dict__.copy()
            user_input['skype'] = changed_skype
            user_input['photo'] = tf
            response = self.client.post(reverse('edit_home'), user_input)
            self.assertContains(response, changed_skype)
            response = self.client.get(reverse('home'))
            self.assertContains(response, file_present_string)
            user_input['skype'] = ''
            response = self.client.post(reverse('edit_home'), user_input)
            self.assertContains(response, 'This field is required')
        # Get Owner object again to ensure file is stored there.
        owner = Owner.objects.filter()[0]
        if not file_present_string in owner.photo.name:
            raise AssertionError('Owner model does not contain uploaded file')

    def test_edit_form_date_widget(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(reverse('edit_home'))
        self.assertContains(response, 'vDateField')  # Widget specific string

    def test_admin_edit_tag(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(reverse('home'))
        self.assertContains(response, '(admin)')  # Tag specific string
        self.assertContains(response, '/admin/hello/owner/1/')  # Tag url rendered

    def test_z_management_command_models_count(self):
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        sys.stderr = cStringIO.StringIO()
        sys.stdout = cStringIO.StringIO()
        call_command('modelcount', [], {})
        self.assertTrue('error: ' in sys.stderr.getvalue())
        self.assertTrue('Model:' in sys.stdout.getvalue())
        self.assertTrue('"owner", Instances: "1"' in sys.stdout.getvalue())
        self.assertTrue('"migration history", Instances: "3"' in sys.stdout.getvalue())
        sys.stderr = old_stderr
        sys.stdout = old_stdout

    def test_signals_processor(self):
        owners = Owner.objects.all()
        logs_before = ModelsLog.objects.all().count()
        owner = owners[0]
        owner.pk += 1
        owner.save()
        logs_after = ModelsLog.objects.all().count()
        self.assertTrue(logs_before < logs_after)
        owner.delete()
        logs_deleted = ModelsLog.objects.all().count()
        self.assertTrue(logs_after < logs_deleted)
        owner = owners[0]
        owner.save()
        logs_final = ModelsLog.objects.all().count()
        self.assertTrue(logs_deleted < logs_final)
