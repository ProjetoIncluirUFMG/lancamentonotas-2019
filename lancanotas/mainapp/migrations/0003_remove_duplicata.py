# Generated by Django 2.2.3 on 2019-07-26 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_muda_turmas'),
    ]

    operations = [
        migrations.RunSQL(
            "DELETE FROM `fechamentoincluir`.`pagamento` WHERE `id_pagamento` = 19387"),
    ]
