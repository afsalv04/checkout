from django import forms
from .models import contact,login

class contactform(forms.ModelForm):
    class Meta:
        model = contact
        fields = ["firstname","lastname","email","message"]  