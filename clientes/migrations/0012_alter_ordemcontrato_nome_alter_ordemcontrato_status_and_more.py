# Generated by Django 5.1.6 on 2025-04-02 19:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_alter_ordemcontrato_etapa'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemcontrato',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ordemcontrato',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('concluido', 'Concluído')], max_length=20),
        ),
        migrations.AlterField(
            model_name='ordemcontrato',
            name='tipo',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='EtapaContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('habilitada', models.BooleanField(default=False)),
                ('concluida', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='ordemcontrato',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens', to='clientes.etapacontrato'),
        ),
    ]
