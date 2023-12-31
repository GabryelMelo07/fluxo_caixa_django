# Generated by Django 4.2.7 on 2023-12-01 16:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacoes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacao',
            name='forma_pagamento',
            field=models.CharField(choices=[('Pix', 'PIX'), ('Cartão', 'CARTÃO'), ('Dinheiro', 'DINHEIRO')], default=django.utils.timezone.now, max_length=8, verbose_name='Forma Pagamento'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='data_hora',
            field=models.DateTimeField(default=None, verbose_name='Data e hora'),
        ),
    ]
