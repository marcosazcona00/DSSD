# Generated by Django 3.2.7 on 2021-10-07 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_auto_20211002_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pais',
            name='nombre_gql',
        ),
        migrations.AlterField(
            model_name='sociosociedadanonima',
            name='sociedad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='models.sociedadanonima'),
        ),
    ]
