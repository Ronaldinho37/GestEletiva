# Generated by Django 5.0.6 on 2024-09-13 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0012_eletivas_img_professores_eletiva'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaginasUtilizaveis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutoria', models.BooleanField()),
                ('eletiva', models.BooleanField()),
                ('index', models.BooleanField()),
            ],
        ),
    ]