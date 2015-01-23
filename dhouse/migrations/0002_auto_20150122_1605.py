# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dhouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersrecord',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 16, 5, 47, 604451), verbose_name=b'record time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ordersrecord',
            name='time_buy',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 16, 5, 47, 604451), verbose_name=b'Buy time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesrecord',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 16, 5, 47, 603912), verbose_name=b'record time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 16, 5, 47, 602942), verbose_name=b'date expired'),
            preserve_default=True,
        ),
    ]
