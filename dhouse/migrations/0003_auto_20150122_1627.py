# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dhouse', '0002_auto_20150122_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersrecord',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 16, 27, 9, 283373), verbose_name=b'record time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ordersrecord',
            name='time_buy',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 16, 27, 9, 283373), verbose_name=b'Buy time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesrecord',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 16, 27, 9, 282795), verbose_name=b'record time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 16, 27, 9, 281799), verbose_name=b'date expired'),
            preserve_default=True,
        ),
    ]
