# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='ammount',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]