# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-11 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0002_recognition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tree',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]