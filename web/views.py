from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Distrito, ZonaUrb, CalleAv, FichaOperativa
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.units import inch
import os

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



from django.shortcuts import get_object_or_404

class FichaOperativaPDFView(View):
    
    def get(self, request, pk, *args, **kwargs):
        # Configuración de la respuesta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ficha_operativa_{pk}.pdf"'

        # Obtener la ficha operativa específica
        ficha = get_object_or_404(FichaOperativa, pk=pk)

        # Crear el PDF
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Estilo del documento
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='TitleStyle',
            parent=styles['Title'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=1,  # Centered
            spaceAfter=12,
            textColor=colors.black
        )
        heading_style = ParagraphStyle(
            name='HeadingStyle',
            parent=styles['Heading2'],
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            alignment=1,  # Centered
            textColor=colors.black
        )
        normal_style = styles['Normal']
        image_style = ParagraphStyle(
            name='ImageStyle',
            fontSize=10,
            spaceAfter=12,
            alignment=1,
            textColor=colors.black
        )

        # Añadir logo en el encabezado
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'logoalto.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2 * inch, height=2* inch)  # Aumentar el tamaño del logo
            elements.append(logo)
            elements.append(Spacer(1, 0.1 * inch))  # Espacio después del logo

        # Título del reporte
        title = Paragraph("Reporte de Ficha Operativa", title_style)
        elements.append(title)
        
        # Añadir espacio después del título
        elements.append(Spacer(1, 0.5 * inch))

        # Crear la tabla para los datos de la ficha operativa
        data = [
            ['Código Usuario:', ficha.codigo.codigo_usuario],
            ['Distrito:', ficha.distrito.nombre if ficha.distrito else 'N/A'],
            ['Zona Urbana:', ficha.zonaurb.nombre if ficha.zonaurb else 'N/A'],
            ['Estado:', ficha.get_estado_display()],
            ['Fecha:', ficha.fecha.strftime('%Y-%m-%d')],
            ['Latitud:', ficha.latitud],
            ['Longitud:', ficha.longitud],
            ['Maquinaria:', ficha.maquinaria or 'N/A'],
            ['Técnico Supervisor:', ficha.tecnico_supervisor.username if ficha.tecnico_supervisor else 'No Asignado'],
            ['Cuadrilla:', ficha.cuadrilla],
            ['Volumen:', ficha.volumen or 'N/A'],
            ['Descripción Trabajo:', ficha.descripcion_trabajo],
        ]

        table = Table(data, colWidths=[2 * inch, 3.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.5 * inch))

        # Añadir las imágenes de la ficha operativa en una sola fila con bordes
        image_data = []
        if ficha.foto_inicio and os.path.exists(ficha.foto_inicio.path):
            image_data.append(Paragraph("Foto Inicio", heading_style))
            image_data.append(Image(ficha.foto_inicio.path, width=1.5 * inch, height=1.5 * inch))
        else:
            image_data.append(Paragraph("Foto Inicio: No Disponible", image_style))
            
        if ficha.foto_desarollo and os.path.exists(ficha.foto_desarollo.path):
            image_data.append(Paragraph("Foto Desarrollo", heading_style))
            image_data.append(Image(ficha.foto_desarollo.path, width=1.5 * inch, height=1.5 * inch))
        else:
            image_data.append(Paragraph("Foto Desarrollo: No Disponible", image_style))
            
        if ficha.foto_culminado and os.path.exists(ficha.foto_culminado.path):
            image_data.append(Paragraph("Foto Culminado", heading_style))
            image_data.append(Image(ficha.foto_culminado.path, width=1.5 * inch, height=1.5 * inch))
        else:
            image_data.append(Paragraph("Foto Culminado: No Disponible", image_style))
        
        if image_data:
            image_table = Table([image_data], colWidths=[2 * inch] * len(image_data))
            image_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))
            elements.append(image_table)
            elements.append(Spacer(1, 0.75 * inch))  # Espacio después de las imágenes

        # Construir el PDF
        doc.build(elements)
        return response

