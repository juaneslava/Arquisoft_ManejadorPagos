from django.db import models
from django_cryptography.fields import encrypt


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
    nombre = models.CharField(max_length= 50)
    porcentaje = models.FloatField(default=0)
    fechaInicio = models.DateField(default='2024-01-01')
    fechaFinal = models.DateField(default='2024-01-01')
    fechaCreacion = models.DateField(auto_now = True)

    def __str__(self):
        return '{}'.format(self.nombre)

class Pago(models.Model):
    nombre = encrypt(models.CharField(null=True,default=None, max_length=50))
    fecha = encrypt(models.DateTimeField(null=True,default=None))
    valor = encrypt(models.FloatField(null=True,default=None))
    interes = encrypt(models.FloatField(null=True,default=None))
    pagado = encrypt(models.BooleanField(null=True,default=None))
    tipo = encrypt(models.CharField(max_length=50, null=True,default=None))
    periodicidad = encrypt(models.IntegerField(null=True,default=None))
    estudiante = (models.ForeignKey(Estudiante, on_delete=models.CASCADE))
    responsableF = (models.ForeignKey(Responsablef, on_delete=models.CASCADE))
    cronograma = (models.ForeignKey(Cronograma, on_delete=models.CASCADE))
    descuento = (models.ForeignKey(Descuento, on_delete=models.SET_NULL, null = True))
    
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
        # Firma ciertos campos antes de guardarlos
        self.nombre = self.nombre
        self.fecha = str(self.fecha)
        self.valor = str(self.valor)
        self.interes = str(self.interes)
        self.pagado = str(self.pagado)
        self.tipo = self.tipo
        self.periodicidad = str(self.periodicidad)
        super().save(*args, **kwargs)
    
# Create your models here.
