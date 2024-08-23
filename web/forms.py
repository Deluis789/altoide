# web/forms.py

from django import forms
from .models import Vecino

class VecinoForm(forms.ModelForm):
    class Meta:
        model = Vecino
        fields = ['usuario', 'codigo_usuario', 'ci']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'codigo_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de Usuario'}),
            'ci': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CIss'}),
        }
