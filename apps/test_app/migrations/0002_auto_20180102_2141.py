# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-02 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_level',
            field=models.IntegerField(),
        ),
    ]
