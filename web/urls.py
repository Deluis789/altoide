from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar, name='registrar'),
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('blog/', views.blog, name='blog'),
]
