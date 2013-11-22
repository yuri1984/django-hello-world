from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db.utils import DatabaseError


class Owner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contacts = models.CharField(max_length=150)
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=30)
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to='pictures', null=True)


class ModelsLog(models.Model):
    model_name = models.CharField(max_length=200)
    action = models.CharField(max_length=50)


def process_model(sender, action):
    # Excluding this model instance
    if not unicode(sender._meta) == u'hello.modelslog':
        try:
            ModelsLog.objects.create(
                model_name=unicode(sender._meta),
                action=action,
            )
        except DatabaseError:
            # Happens when you try to store model instance while making first syncdb
            pass



@receiver(pre_save)
def update_callback(sender, instance, **kwargs):
    if 'id' in instance.__dict__:
        if instance.id is not None:
            process_model(sender, 'model update')

@receiver(post_save)
def save_callback(sender, **kwargs):
    process_model(sender, 'model save')

@receiver(post_delete)
def delete_callback(sender, **kwargs):
    process_model(sender, 'model delete')
