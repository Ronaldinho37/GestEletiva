# Generated by Django 5.0.6 on 2024-11-05 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0018_remove_carrosselprofessores_ids_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarrosseldosProfessores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('graduacao', models.CharField(max_length=100)),
                ('imagem', models.FileField(upload_to='carrosselProfessores/')),
                ('descricao', models.TextField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='CarrosselProfessores',
        ),
    ]
