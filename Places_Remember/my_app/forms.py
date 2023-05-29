from django import forms
from .models import *

class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'comment']