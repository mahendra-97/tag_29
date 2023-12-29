from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class tags_form(forms.Form):

    # Form for handling tag-related data.
    tag_name = forms.CharField(required=False, min_length=1, max_length=50)
    scope = forms.CharField(required=False, min_length=1, max_length=50)

class VMForm(forms.Form):

    # Form for handling virtual machine (VM) related data.
    vm_name = forms.CharField(required=True, min_length=1, max_length=255)
    tag_name = forms.CharField(required=False, min_length=1, max_length=50)
    scope = forms.CharField(required=False, min_length=1, max_length=50)
