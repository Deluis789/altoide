from django.db import models
from django.contrib.auth.models import User, Group
import random
import string
# Create your models here.

def generate_random_code(length=6):
    """Genera un código alfanumérico aleatorio de la longitud especificada."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class Distrito(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.TextField(null=True)
    
    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"

    def __str__(self):
        return self.nombre

class ZonaUrb(models.Model):
    nombre = models.CharField(max_length=80, null=False, blank=False)
    descripcion = models.TextField()
    ciudad = models.CharField(max_length=50, default='El alto')
    cordenadas = models.CharField(max_length=50, null=False, blank=False)
    distrito = models.ForeignKey(Distrito, on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = "Zona/Urb."
        verbose_name_plural = "Zonas/Urb."
        
    def __str__(self):
        return self.nombre
    
class CalleAv(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField(null=True)
    numero_vivienda = models.IntegerField(null=False, blank=False)
    zona_urb = models.ForeignKey(ZonaUrb, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Calle/Avenida"
        verbose_name_plural = "Calles/Avenidas"
        
    def __str__(self):
        return self.nombre

    
class Usuariosp(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.RESTRICT)
    nombres = models.CharField(max_length=50, null=False, blank=False)
    apellido_paterno = models.CharField(max_length=50, null=False, blank=False)
    apellido_materno = models.CharField(max_length=50, null=False, blank=False)
    codigo_usuario = models.CharField(max_length=8, null=False, blank=False, unique=True)
    ci = models.CharField(max_length=10, null=False, blank=False)
    Zona_urb = models.ForeignKey(ZonaUrb, on_delete=models.RESTRICT)
    Calle_av = models.ForeignKey(CalleAv, on_delete=models.RESTRICT)
    numero_vivienda = models.IntegerField()
    grupos = models.ManyToManyField(Group, blank=True)  # Relación con Group
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    def save(self, *args, **kwargs):
        # Si el código_usuario está vacío (es decir, estamos creando un nuevo Vecino)
        if not self.codigo_usuario: 
            # Genera un código aleatorio
            self.codigo_usuario = generate_random_code()
            # Asegúrate de que el código sea único
            while Usuariosp.objects.filter(codigo_usuario=self.codigo_usuario).exists():
                self.codigo_usuario = generate_random_code()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.codigo_usuario
    
        
class SolicitudVecino(models.Model):
    vecino = models.ForeignKey(Usuariosp, on_delete=models.RESTRICT)
    distrito = models.ForeignKey(Distrito, on_delete=models.RESTRICT)
    zona_urbanizacion = models.ForeignKey(ZonaUrb, on_delete=models.RESTRICT)
    fecha = models.DateField(auto_now_add=True)
    foto_solicitud = models.ImageField(upload_to='trabajo', blank=True)
    ubicacion_direccion = models.CharField(max_length=100, null=False, blank=False)
    latitud = models.FloatField(null=True, blank=True, default=-16.500000)
    longitud = models.FloatField(null=True, blank=True, default=-68.150000)
    celular = models.IntegerField()
    
    class Meta:
        verbose_name = "SolicitudVecino"
        verbose_name_plural = "Solicitudes/Vecinos"

    def __str__(self):
        try:
            return self.vecino.codigo_usuario
        except AttributeError as e:
            return f"Error: {e} - {self.vecino} - {self.distrito} - {self.ubicacion_direccion}"
    
    def get_google_maps_url(self):
        if self.latitud and self.longitud:
            return f"https://www.google.com/maps?q={self.latitud},{self.longitud}"
        return None


    
class FichaOperativa(models.Model):

    ESTADO_OPCIONES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    codigo = models.ForeignKey(Usuariosp, on_delete=models.RESTRICT)  
    fecha = models.DateField(auto_now_add=True)  
    distrito = models.ForeignKey(Distrito, on_delete=models.RESTRICT)
    zonaurb = models.ForeignKey(ZonaUrb, on_delete=models.RESTRICT)
    latitud = models.FloatField(null=True, blank=True, default=-16.500000)
    longitud = models.FloatField(null=True, blank=True, default=-68.150000)
    maquinaria = models.CharField(max_length=50, null=True, blank=True)
    tecnico_supervisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    cuadrilla = models.CharField(max_length=100)
    volumen = models.CharField(max_length=100, null=True, blank=True)
    descripcion_trabajo = models.TextField(default='Descripcion...')
    foto_inicio = models.ImageField(upload_to='trabajo', blank=True)
    foto_desarollo = models.ImageField(upload_to='trabajo', blank=True)
    foto_culminado = models.ImageField(upload_to='trabajo', blank=True)
    estado = models.CharField(max_length=30, choices=ESTADO_OPCIONES, default='pendiente')

    class Meta:
        verbose_name = "Ficha Técnica"
        verbose_name_plural = "Fichas Técnicas"

    def __Str__(self):
        return f'{self.codigo} - {self.get_estado_display()}'
    
class Solicitudes(models.Model):
    ESTADO_OPCIONES = [
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('desechado', 'Desechado'),
    ]
    
    solicitud_vecino = models.ForeignKey(SolicitudVecino, on_delete=models.RESTRICT)  # Relación con SolicitudVecino
    distrito = models.ForeignKey(Distrito, on_delete=models.RESTRICT)
    zonaurb = models.ForeignKey(ZonaUrb, on_delete=models.RESTRICT)
    fecha = models.DateField(auto_now_add=True, blank=False)  
    estado = models.CharField(max_length=30, choices=ESTADO_OPCIONES)
    asignacion = models.ForeignKey(Usuariosp, on_delete=models.RESTRICT, related_name="solicitudes_asignadas")  # Asignación a un usuario

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f'Solicitud de {self.solicitud_vecino.vecino.codigo_usuario} - {self.get_estado_display()}'
