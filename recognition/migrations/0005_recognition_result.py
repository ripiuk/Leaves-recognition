# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-11 00:25
from __future__ import unicode_literals

from django.db import migrations, models
import recognition.models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0004_auto_20170611_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='recognition',
            name='result',
            field=models.CharField(max_length=250, null=recognition.models.Tree),
        ),
    ]
