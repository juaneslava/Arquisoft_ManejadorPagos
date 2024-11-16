import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pago, Estudiante, Responsablef, Cronograma, Descuento
from django.core.signing import BadSignature
from django.contrib.auth.decorators import login_required
from manejador_pagos.auth0backend import getRole
import json

def inicio(request):
    return HttpResponse("Bienvenido al manejador de pagos")

def formulario_pago(request):
    return render(request, 'formulario_pago.html')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)

def obtenerpagos(request):
    if request.method== 'GET':
        #try:
        pagos = Pago.objects.all()
        for pago in pagos:
            print(pagos.query)
            print(pagos)
        pagos_list = list(pagos.values())  # Convierte el queryset en una lista de diccionarios
        return JsonResponse(pagos_list, safe=False)
        #except BadSignature as e:
        #    return JsonResponse({"error": "error descifrando registro"}, status=405)



#@login_required
def crear_pago(request):
    if request.method == 'POST':
        role = getRole(request)  # Asegúrate de que esta función está definida y funciona correctamente.
        if role in ["Responsable financiero", "Administrador"]:
            try:
                # Verifica si los datos vienen en formato JSON
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                else:
                    data = request.POST
                
                # Valida la presencia de los campos necesarios
                estudiante = Estudiante.objects.get(id=data['estudiante_id'])
                responsable = Responsablef.objects.get(id=data['responsablef_id'])
                cronograma = Cronograma.objects.get(id=data['cronograma_id'])
                
                # Manejo del campo "descuento" (opcional)
                descuento = None
                if 'descuento_id' in data and data['descuento_id']:
                    descuento = Descuento.objects.get(id=data['descuento_id'])

                # Conversión de valores
                pagado = data.get('pagado') == 'on'
                
                # Valida y convierte la fecha
                try:
                    fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return JsonResponse({"error": "Formato de fecha inválido. Use 'YYYY-MM-DD HH:MM:SS'."}, status=400)

                # Crear el pago
                pago = Pago.objects.create(
                    nombre=data['nombre'],
                    fecha=fecha,
                    valor=float(data['valor']),
                    interes=float(data['interes']),
                    pagado=pagado,
                    tipo=data['tipo'],
                    periodicidad=int(data['periodicidad']),
                    estudiante=estudiante,
                    responsableF=responsable,
                    cronograma=cronograma,
                    descuento=descuento,
                )
                return JsonResponse({"mensaje": "Pago creado con éxito", "pago_id": pago.id}, status=201)
            
            except Estudiante.DoesNotExist:
                return JsonResponse({"error": "Estudiante no encontrado"}, status=404)
            except Responsablef.DoesNotExist:
                return JsonResponse({"error": "Responsable financiero no encontrado"}, status=404)
            except Cronograma.DoesNotExist:
                return JsonResponse({"error": "Cronograma no encontrado"}, status=404)
            except Descuento.DoesNotExist:
                return JsonResponse({"error": "Descuento no encontrado"}, status=404)
            except KeyError as e:
                return JsonResponse({"error": f"Falta el campo requerido: {str(e)}"}, status=400)
            except Exception as e:
                return JsonResponse({"error": f"Error desconocido: {str(e)}"}, status=500)

        return JsonResponse({"error": "Permiso denegado"}, status=403)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def obtenerpagos(request):
    role = getRole(request)
    if role == "Administrador":
        if request.method== 'GET':
            pagos = Pago.objects.all()
            pagos_list = list(pagos.values())  # Convierte el queryset en una lista de diccionarios
            return JsonResponse(pagos_list, safe=False)
        


# Create your views here.
