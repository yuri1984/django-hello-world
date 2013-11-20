from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from models import Owner


class EditOwner(forms.ModelForm):
    date_of_birth = forms.DateField(widget=AdminDateWidget)
    class Meta:
        model = Owner