# Generated by Django 5.0.6 on 2024-09-13 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0013_paginasutilizaveis'),
    ]

    operations = [
        migrations.AddField(
            model_name='paginasutilizaveis',
            name='sobre',
            field=models.BooleanField(null=True),
        ),
    ]