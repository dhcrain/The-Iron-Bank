# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-28 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0002_auto_20160620_1933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('+', 'Deposit'), ('-', 'Debit')], max_length=6),
        ),
    ]
