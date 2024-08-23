from django import forms
from django.contrib.auth.models import User, Group
from .models import Usuariosp, Solicitudes, FichaOperativa

class UsuariospForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label='Usuario',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label='Rol',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})  # Cambio aquí
    )

    class Meta:
        model = Usuariosp
        fields = ['usuario', 'codigo_usuario','nombres', 'apellido_paterno','apellido_materno','ci', 'Zona_urb', 'Calle_av', 'numero_vivienda', 'grupos']
        widgets = {
            'codigo_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de Usuario'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'ci': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CI'}),
            'Zona_urb': forms.Select(attrs={'class': 'form-control'}),
            'Calle_av': forms.Select(attrs={'class': 'form-control'}),
            'numero_vivienda': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de Vivienda'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Inicializa los campos relacionados con el usuario
            self.fields['usuario'].initial = self.instance.usuario
            self.fields['grupos'].initial = self.instance.grupos.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = self.cleaned_data['usuario']
        user.username = self.cleaned_data['usuario'].username
        user.first_name = self.cleaned_data['usuario'].first_name
        user.last_name = self.cleaned_data['usuario'].last_name
        if commit:
            user.save()
            instance.usuario = user
            instance.save()
            instance.grupos.set(self.cleaned_data['grupos'])
        return instance

class SolicitudesForm(forms.ModelForm):
    class Meta:
        model = Solicitudes
        fields = ['solicitud_vecino', 'distrito', 'zonaurb', 'estado', 'asignacion']
        widgets = {
            'solicitud_vecino': forms.Select(attrs={'class': 'form-control'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'zonaurb': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=Solicitudes.ESTADO_OPCIONES, attrs={'class': 'form-control'}),
            'asignacion': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'solicitud_vecino': 'Vecino Solicitante',
            'distrito': 'Distrito',
            'zonaurb': 'Zona de Urbanización',
            'estado': 'Estado de Solicitud',
            'asignacion': 'Asignado a',
        }
        help_texts = {
            'solicitud_vecino': 'Selecciona el vecino que realiza la solicitud.',
            'distrito': 'Selecciona el distrito relacionado.',
            'zonaurb': 'Selecciona la zona de urbanización correspondiente.',
            'estado': 'Estado actual de la solicitud.',
            'asignacion': 'Selecciona el usuario al que se asignará la solicitud.',
        }

class FichaOperativaForm(forms.ModelForm):
    class Meta:
        model = FichaOperativa
        fields = [
            'codigo', 'distrito', 'zonaurb', 'latitud', 'longitud', 'maquinaria', 
            'tecnico_supervisor', 'cuadrilla', 'volumen', 'descripcion_trabajo',
            'foto_inicio', 'foto_desarollo', 'foto_culminado', 'estado'
        ]
        widgets = {
            'codigo': forms.Select(attrs={'class': 'form-control'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'zonaurb': forms.Select(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'maquinaria': forms.TextInput(attrs={'class': 'form-control'}),
            'tecnico_supervisor': forms.Select(attrs={'class': 'form-control'}),
            'cuadrilla': forms.TextInput(attrs={'class': 'form-control'}),
            'volumen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'foto_inicio': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'foto_desarollo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'foto_culminado': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'codigo': 'Código de Usuario',
            'distrito': 'Distrito',
            'zonaurb': 'Zona Urbana',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'maquinaria': 'Maquinaria Utilizada',
            'tecnico_supervisor': 'Técnico Supervisor',
            'cuadrilla': 'Cuadrilla',
            'volumen': 'Volumen de Trabajo',
            'descripcion_trabajo': 'Descripción del Trabajo',
            'foto_inicio': 'Foto al Inicio',
            'foto_desarollo': 'Foto en Desarrollo',
            'foto_culminado': 'Foto al Culminar',
            'estado': 'Estado de la Ficha',
        }
        help_texts = {
            'latitud': 'Ingresa la latitud del lugar de trabajo. Ejemplo: -16.500000',
            'longitud': 'Ingresa la longitud del lugar de trabajo. Ejemplo: -68.150000',
            'foto_inicio': 'Sube una foto del estado inicial del trabajo.',
            'foto_desarollo': 'Sube una foto del desarrollo del trabajo.',
            'foto_culminado': 'Sube una foto del trabajo completado.',
        }
