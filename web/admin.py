from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group, User
from .models import (Usuariosp, Distrito, ZonaUrb, CalleAv, SolicitudVecino, Solicitudes,FichaOperativa, generate_random_code)
from .forms import UsuariospForm, SolicitudesForm, FichaOperativaForm
from django.contrib.auth.admin import GroupAdmin, UserAdmin as DefaultUserAdmin

# Personaliza la administración del modelo Group
class CustomGroupAdmin(GroupAdmin):
    list_display = ('id', 'name')  # Mostrar ID y nombre en la lista
    search_fields = ('name',)     # Permitir búsqueda por nombre

# Verifica si el modelo ya está registrado antes de intentar registrarlo
if not admin.site.is_registered(Group):
    admin.site.register(Group, CustomGroupAdmin)
    


# Extender la clase UserAdmin predeterminada

class CustomUserAdmin(DefaultUserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    # Campos que se mostrarán en el formulario de detalle del usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ('user_permissions', 'groups')

    # Especificar la plantilla personalizada
    change_list_template = 'admin/usuarios.html'

# Desregistrar el admin predeterminado y registrar el admin personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
    
class HiddenModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  # Oculta el modelo de la interfaz de administración

# Mantén tu lógica personalizada para cada modelo aquí
class SolicitudVecinoAdmin(HiddenModelAdmin):
    list_display = ('vecino_codigo_usuario', 'distrito', 'zona_urbanizacion', 'ubicacion_direccion', 'latitud', 'longitud', 'foto_solicitud', 'celular', 'google_maps_link')
    search_fields = ('vecino__codigo_usuario', 'ubicacion_direccion', 'distrito__nombre', 'zona_urbanizacion__nombre')
    list_filter = ('distrito', 'zona_urbanizacion')
    ordering = ('fecha',)
    
    fieldsets = (
        (None, {
            'fields': ('vecino', 'distrito', 'zona_urbanizacion', 'ubicacion_direccion', 'celular', 'foto_solicitud', 'latitud', 'longitud')
        }),
    )
    
    def vecino_codigo_usuario(self, obj):
        return obj.vecino.codigo_usuario if obj.vecino else 'Sin Código'
    vecino_codigo_usuario.short_description = 'Código de Usuario'

    def google_maps_link(self, obj):
        if obj.latitud and obj.longitud:
            url = obj.get_google_maps_url()
            return format_html(f'<a href="{url}" target="_blank">Ver en Google Maps</a>')
        return '-'
    google_maps_link.short_description = 'Ubicación en el mapa'
    

class UsuariospAdmin(HiddenModelAdmin):
    form = UsuariospForm
    list_display = [field.name for field in Usuariosp._meta.fields]
    readonly_fields = ('codigo_usuario',)
    change_list_template = 'admin/usuariospi.html'

    def save_model(self, request, obj, form, change):
        if not obj.codigo_usuario:
            obj.codigo_usuario = generate_random_code()
        super().save_model(request, obj, form, change)

class ZonaUrbAdmin(HiddenModelAdmin):
    list_display = [field.name for field in ZonaUrb._meta.fields]

class DistritoAdmin(HiddenModelAdmin):
    list_display = [field.name for field in Distrito._meta.fields]

class CalleAvAdmin(HiddenModelAdmin):
    list_display = [field.name for field in CalleAv._meta.fields]

class FichaOperativaAdmin(HiddenModelAdmin):
    form = FichaOperativaForm  # Usar el formulario personalizado

    # Mostrar campos específicos en la lista de elementos
    list_display = ['codigo', 'distrito', 'zonaurb', 'fecha', 'estado', 'tecnico_supervisor']

    # Agregar filtros laterales para facilitar la búsqueda
    list_filter = ['distrito', 'zonaurb', 'estado', 'tecnico_supervisor', 'fecha']

    # Habilitar la búsqueda por ciertos campos
    search_fields = ['codigo__codigo_usuario', 'cuadrilla', 'descripcion_trabajo']

    # Campos que se mostrarán en la vista de detalles del modelo
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'distrito', 'zonaurb', 'estado', 'fecha')
        }),
        ('Detalles del Trabajo', {
            'fields': ('latitud', 'longitud', 'maquinaria', 'tecnico_supervisor', 'cuadrilla', 'volumen', 'descripcion_trabajo')
        }),
        ('Fotos del Proceso', {
            'fields': ('foto_inicio', 'foto_desarollo', 'foto_culminado')
        }),
    )

    # Hacer que algunos campos sean de solo lectura
    readonly_fields = ['fecha']
    change_list_template = 'admin/fichas.html'
    
class SolicitudesAdmin(HiddenModelAdmin):
    form = SolicitudesForm
    list_display = ['solicitud_vecino', 'distrito', 'zonaurb', 'fecha', 'estado', 'asignacion']
    search_fields = ['solicitud_vecino__vecino__codigo_usuario', 'distrito__nombre', 'zonaurb__nombre', 'estado']
    list_filter = ['estado', 'distrito', 'zonaurb']
    date_hierarchy = 'fecha'
    
    change_list_template = 'admin/solicitudes.html'
    # Marca el campo 'fecha' como de solo lectura

admin.site.register(Solicitudes, SolicitudesAdmin)


# Registra los modelos con las lógicas personalizadas y con HiddenModelAdmin para ocultarlos
admin.site.register(Usuariosp, UsuariospAdmin)
admin.site.register(ZonaUrb, ZonaUrbAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(CalleAv, CalleAvAdmin)
admin.site.register(SolicitudVecino, SolicitudVecinoAdmin)
admin.site.register(FichaOperativa, FichaOperativaAdmin)
# admin.site.register(Solicitudes, SolicitudesAdmin)
