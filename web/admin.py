from django.contrib import admin
from django.utils.html import format_html
from .models import (SolicitudVecino, Vecino, Distrito, ZonaUrb, CalleAv, FichaOperativa, Solicitudes, generate_random_code)
from .forms import VecinoForm

class HiddenModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  # Oculta el modelo de la interfaz de administración

# Mantén tu lógica personalizada para cada modelo aquí
class SolicitudVecinoAdmin(HiddenModelAdmin):
    list_display = ('vecino', 'distrito', 'zona_urbanizacion', 'ubicacion_direccion', 'latitud', 'longitud', 'celular', 'google_maps_link')
    search_fields = ('vecino__codigo_usuario', 'ubicacion_direccion', 'distrito__nombre', 'zona_urbanizacion__nombre')
    list_filter = ('distrito', 'zona_urbanizacion')
    ordering = ('fecha',)
    
    fieldsets = (
        (None, {
            'fields': ('vecino', 'distrito', 'zona_urbanizacion', 'ubicacion_direccion', 'celular', 'latitud', 'longitud')
        }),
    )

    def google_maps_link(self, obj):
        if obj.latitud and obj.longitud:
            url = obj.get_google_maps_url()
            return format_html(f'<a href="{url}" target="_blank">Ver en Google Maps</a>')
        return '-'
    google_maps_link.short_description = 'Ubicación en el mapa'

class VecinoAdmin(HiddenModelAdmin):
    form = VecinoForm
    list_display = [field.name for field in Vecino._meta.fields]
    readonly_fields = ('codigo_usuario',)

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
    list_display = [field.name for field in FichaOperativa._meta.fields]

class SolicitudesAdmin(HiddenModelAdmin):
    list_display = [field.name for field in Solicitudes._meta.fields]

# Registra los modelos con las lógicas personalizadas y con HiddenModelAdmin para ocultarlos
admin.site.register(SolicitudVecino, SolicitudVecinoAdmin)
admin.site.register(Vecino, VecinoAdmin)
admin.site.register(ZonaUrb, ZonaUrbAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(CalleAv, CalleAvAdmin)
admin.site.register(FichaOperativa, FichaOperativaAdmin)
admin.site.register(Solicitudes, SolicitudesAdmin)
