import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

class SociedadAnonima(models.Model):
    class Meta:
        db_table = 'SociedadAnonima'
    nombre = models.CharField(max_length = 255, null = False)
    fecha_creacion = models.DateField(null=False)
    estatuto = models.FileField(null = False)
    domicilio_real = models.CharField(max_length = 255, null = False)
    domicilio_legal = models.CharField(max_length = 255, null = False)
    email_apoderado = models.EmailField()
    apoderado = models.OneToOneField('SocioSociedadAnonima', null = False, on_delete = models.CASCADE)
    paises_exporta = models.ManyToManyField('Pais')

class SocioSociedadAnonima(models.Model):
    class Meta:
        db_table = 'SocioSociedadAnonima'
    nombre = models.CharField(max_length = 255, null = False)
    apellido = models.CharField(max_length = 255 , null = False)
    porcentaje_aporte = models.FloatField()
    sociedad = models.OneToOneField(SociedadAnonima, null = True, on_delete = models.CASCADE) #Si es null, entonces es un apoderado

class Pais(models.Model):
    class Meta:
        db_table = 'Pais'
    codigo_gql = models.CharField(max_length = 255, null = False)



