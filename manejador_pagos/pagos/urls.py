from django.urls import path
from . import views

urlpatterns = [
    path('crear_pago/', views.crear_pago, name='crear_pago'),
    path('formulario_pago/', views.formulario_pago, name='formulario_pago'),
    path('obtener_pagos',views.obtenerpagos, name='obtener_pago'),
]
