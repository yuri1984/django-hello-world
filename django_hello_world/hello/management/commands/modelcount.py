from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app, get_models
from django.conf import settings


class Command(BaseCommand):
    args = ''
    help = 'Iterates through INSTALLED_APPS and prints out models instances count.'

    def handle(self, *args, **opts):
        apps = settings.INSTALLED_APPS
        for app_name in apps:
            app = None
            try:
                app = get_app(app_name)
            except ImproperlyConfigured, e:
                self.stderr.write('error: Can not resolve model in app: "%s", error: %s\n' % (app_name, e))
                pass
            if app is not None:
                for model in get_models(app):
                    model_cnt = model.objects.count()
                    model_name = model._meta.verbose_name
                    self.stdout.write('App: "%s", Model: "%s", Instances: "%s"\n' % (app_name, model_name, model_cnt))
