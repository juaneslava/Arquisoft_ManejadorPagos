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
    nombre = models.CharField(max_length= 50)
    porcentaje = models.FloatField(default=0)
    fechaInicio = models.DateField(default='2024-01-01')
    fechaFinal = models.DateField(default='2024-01-01')
    fechaCreacion = models.DateField(auto_now = True)

    def __str__(self):
        return '{}'.format(self.nombre)

class Pago(models.Model):
    nombre = encrypt(models.CharField(null=True,default=None, max_length=50))
    fecha = (models.DateTimeField(null=True,default=None))
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
    
class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('nombre', models.CharField(null=True,default=None,max_length=50)),
                ('fecha', models.DateTimeField(null=True,default=None)),
                ('valor', models.FloatField(null=True,default=None)),
                ('interes',models.FloatField(null=True,default=None)),
                ('pagado', models.BooleanField(null=True,default=None)),
                ('tipo', models.CharField(max_length=50, null=True,default=None)),
                ('periodicidad', models.IntegerField(null=True,default=None))
            ],
        ),
    ]

class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encryptedcharmodel',
            old_name='field',
            new_name='old_field',
        ),
    ]

class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0002_rename_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='encryptedcharmodel',
            name='field',
            field= django_cryptography.fields.encrypt(
                models.CharField(default=None, max_length=50)),
            preserve_default=False,
        ),
    ]

def forwards_encrypted_char(apps, schema_editor):
    EncryptedCharModel = apps.get_model("fields", "EncryptedCharModel")

    for row in EncryptedCharModel.objects.all():
        row.field = row.old_field
        row.save(update_fields=["field"])


def reverse_encrypted_char(apps, schema_editor):
    EncryptedCharModel = apps.get_model("fields", "EncryptedCharModel")

    for row in EncryptedCharModel.objects.all():
        row.old_field = row.field
        row.save(update_fields=["old_field"])


class Migration(migrations.Migration):

    dependencies = [
        ("fields", "0003_add_encrypted_fields"),
    ]

    operations = [
        migrations.RunPython(forwards_encrypted_char, reverse_encrypted_char),
    ]
# Create your models here.
