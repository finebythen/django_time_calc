from django.forms import ModelForm
from .models import *


class CreateTimeEntryForm(ModelForm):
    class Meta:
        model = TimeEntry
        fields = [
            'key_values',
        ]
