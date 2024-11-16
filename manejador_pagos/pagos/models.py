from django.db import models
import django_cryptography
from django_cryptography.fields import encrypt
from django.db import migrations


class Institucion(models.Model):
    nombre = models.CharField(max_length=50)
    logo = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    def __str__(self):
        return '{}'.format(self.nombre)

class Estudiante(models.Model):
    codigo = models.IntegerField(default=1)
    nombre = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE )

    def __str__(self):
        return '{}'.format(self.nombre)

class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    correo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE )

    def __str__(self):
        return '{}'.format(self.nombre)
    
class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    estudiantes = models.ManyToManyField(Estudiante)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    

    def __str__(self):
        return '{}'.format(self.nombre)

class Responsablef(Usuario):
    estudiantes = models.ManyToManyField(Estudiante)
    def __str__(self):
        return '{}'.format(self.nombre)
    
class Cronograma(models.Model):
    anio = models.IntegerField(default=2024)
    nombre = models.CharField(max_length= 100)
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

class Descuento(models.Model):
    porcentaje = models.FloatField(default=0)
    fechaInicio = models.DateField(default='2024-01-01')
    fechaFinal = models.DateField(default='2024-01-01')
    fechaCreacion = models.DateField()

    def __str__(self):
        return '{}'.format(self.nombre)

class Pago(models.Model):
    nombre = (models.CharField(null=True,default=None, max_length=50))
    fecha = (models.DateTimeField(null=True,default=None))
    valor = (models.FloatField(null=True,default=None))
    interes = (models.FloatField(null=True,default=None))
    pagado = (models.BooleanField(null=True,default=None))
    tipo = (models.CharField(max_length=50, null=True,default=None))
    periodicidad = (models.IntegerField(null=True,default=None))
    estudiante = (models.ForeignKey(Estudiante, on_delete=models.CASCADE))
    responsableF = (models.ForeignKey(Responsablef, on_delete=models.CASCADE))
    cronograma = (models.ForeignKey(Cronograma, on_delete=models.CASCADE))
    descuento = (models.ForeignKey(Descuento, on_delete=models.SET_NULL, null = True))
    
    def __str__(self):
        return '{}'.format(self.nombre)

    
# Create your models here.
