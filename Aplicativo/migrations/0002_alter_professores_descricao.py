# Generated by Django 5.1.3 on 2024-11-12 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professores',
            name='descricao',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
