# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(verbose_name=b'number of product')),
                ('time', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 16, 2, 0, 196475), verbose_name=b'record time')),
                ('time_buy', models.DateTimeField(default=datetime.datetime(2015, 1, 25, 16, 2, 0, 196475), verbose_name=b'Buy time')),
                ('state', models.BooleanField(default=False)),
                ('money', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('discount', models.FloatField(default=1)),
                ('photo', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=600)),
                ('remains', models.IntegerField()),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(verbose_name=b'number of product')),
                ('time', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 16, 2, 0, 195923), verbose_name=b'record time')),
                ('money', models.FloatField(default=0)),
                ('product', models.ForeignKey(to='dhouse.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(default=b'M', max_length=2, choices=[('M', 'Male'), ('F', 'Female')])),
                ('addr', models.CharField(max_length=200, null=True, verbose_name=b'address')),
                ('money', models.FloatField(default=0.0)),
                ('level', models.IntegerField(default=0)),
                ('state', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(default=datetime.datetime(2016, 1, 22, 16, 2, 0, 194962), verbose_name=b'date expired')),
                ('products', models.ManyToManyField(to='dhouse.Product', null=True, through='dhouse.SalesRecord')),
                ('products_order', models.ManyToManyField(related_name='users_order', null=True, through='dhouse.OrdersRecord', to='dhouse.Product')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='salesrecord',
            name='user',
            field=models.ForeignKey(to='dhouse.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersrecord',
            name='product',
            field=models.ForeignKey(to='dhouse.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordersrecord',
            name='user',
            field=models.ForeignKey(to='dhouse.UserProfile'),
            preserve_default=True,
        ),
    ]
