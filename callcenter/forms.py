from django import forms
from .models import *


class UploadForm(forms.ModelForm):

    class Meta:
        model = Uploades
        fields = '__all__'


class CallerForm(forms.ModelForm):

    class Meta:
        model = Caller
        fields = '__all__'

