# Generated by Django 5.1.6 on 2025-04-01 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_alter_ordemcontrato_nome_alter_ordemcontrato_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemcontrato',
            name='etapa',
            field=models.IntegerField(default=1),
        ),
    ]
