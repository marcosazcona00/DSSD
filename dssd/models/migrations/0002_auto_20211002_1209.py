# Generated by Django 3.2.7 on 2021-10-02 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pais',
            options={'verbose_name': 'Pais'},
        ),
        migrations.AlterModelOptions(
            name='sociedadanonima',
            options={'verbose_name': 'SociedadAnonima'},
        ),
        migrations.AlterModelOptions(
            name='sociosociedadanonima',
            options={'verbose_name': 'SocioSociedadAnonima'},
        ),
    ]
