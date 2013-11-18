from django import forms
from models import Owner


class EditOwner(forms.ModelForm):
    class Meta:
        model = Owner