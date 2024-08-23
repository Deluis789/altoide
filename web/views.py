from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Vecino, Distrito, ZonaUrb, CalleAv, SolicitudVecino, FichaOperativa, Solicitudes
from django.contrib.auth import login, logout, authenticate

# VISTAS PARA CLIENTES Y USUARIOS
def index(request):
    return render(request, 'index.html', {})


def crearUsuario(request):
    if request.method == 'POST':
        dataUsuario = request.POST['name']
        dataPassword = request.POST['password']
        
        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        
        if nuevoUsuario is not None:
            login(request, nuevoUsuario)
            return redirect('web:registrar')
            
    return render(request, 'usuario/login.html')
    
            
def registrar(request):
    return render(request, 'usuario/formulario.html', {})

def blog(request):
    return render(request, 'blog.html', {})
