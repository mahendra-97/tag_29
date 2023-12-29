from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
# from django.contrib.postgres.forms import SimpleArrayField
# from django.conf import settings as conf_settings
from django.core.validators import RegexValidator

class tags_form(forms.Form):
    tag_name = forms.CharField(required=False,min_length=1,max_length=50)
    scope = forms.CharField(required=False,min_length=1,max_length=50)

class VMForm(forms.Form):
    vm_name = forms.CharField(required=True,min_length=255)
    tag_name = forms.CharField(required=False,min_length=1,max_length=50)
    scope = forms.CharField(required=False,min_length=1,max_length=50)

