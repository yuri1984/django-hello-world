"""Template context processors for 42-test-garmoncheg"""

from django.conf import settings


def django_settings(context):
    """Provides Django Settings for interactions in templates"""
    return {'django_settings': settings}