# Generated by Django 5.1.6 on 2025-04-10 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0015_faseprocesso'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faseprocesso',
            options={},
        ),
        migrations.AlterField(
            model_name='faseprocesso',
            name='numero',
            field=models.IntegerField(),
        ),
    ]
