# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='des_img',
            field=models.ImageField(blank=True, upload_to='polls/uploads/'),
        ),
    ]