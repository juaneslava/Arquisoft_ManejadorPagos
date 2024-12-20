from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pago, Estudiante, Responsablef, Cronograma, Descuento
from django.contrib.auth.decorators import login_required
from manejador_pagos.auth0backend import getRole
import json

def inicio(request):
    return HttpResponse("Bienvenido al manejador de pagos")

def formulario_pago(request):
    return render(request, 'formulario_pago.html')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)

@csrf_exempt
@login_required
def crear_pago(request):
    if request.method == 'POST':
        role = getRole(request)
        if role == "Responsable financiero" or role == "Administrador":
            try:
                # Verifica si los datos vienen de un formulario (POST clásico) o en formato JSON
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                else:
                    data = request.POST
                
                estudiante = Estudiante.objects.get(id=data['estudiante_id'])
                responsable = Responsablef.objects.get(id=data['responsablef_id'])
                cronograma = Cronograma.objects.get(id=data['cronograma_id'])
                
                # Manejo del campo "descuento" (es opcional)
                descuento = None
                if 'descuento_id' in data and data['descuento_id']:
                    descuento = Descuento.objects.get(id=data['descuento_id'])

                pagado = True if data.get('pagado') == 'on' else False

                # Crear el pago
                pago = Pago.objects.create(
                    nombre=data['nombre'],
                    fecha=data['fecha'],
                    valor=data['valor'],
                    interes=data['interes'],
                    pagado=pagado,
                    tipo=data['tipo'],
                    periodicidad=data['periodicidad'],
                    estudiante=estudiante,
                    responsableF=responsable,
                    cronograma=cronograma,
                    descuento=descuento,
                )
                return JsonResponse({"mensaje": "Pago creado con exito", "pago_id": pago.id}, status=201)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)

@login_required
def obtenerpagos(request):
    role = getRole(request)
    if role == "Administrador":
        if request.method== 'GET':
            pagos = Pago.objects.all()
            pagos_list = list(pagos.values())  # Convierte el queryset en una lista de diccionarios
            return JsonResponse(pagos_list, safe=False)



        
def traerPagos(Cronograma, fecha):
    pagos = Pago.objects.filter(cronograma = Cronograma, fecha = fecha).all()
    context = list(queryset.values('id', 'name'))
    return JsonResponse(context, safe=False)
    # Create your views here.
