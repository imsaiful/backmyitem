# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-26 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0017_auto_20180827_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report_item',
            name='location',
            field=models.CharField(help_text='*Enter the address and city where you found this item', max_length=255),
        ),
    ]
