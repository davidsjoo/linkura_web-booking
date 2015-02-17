# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=50)),
                ('client_mail', models.EmailField(max_length=100)),
                ('client_phone', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(verbose_name=b'Date and time')),
                ('capacity', models.IntegerField(default=1)),
                ('location', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visit_name', models.CharField(max_length=50)),
                ('visit_date', models.DateTimeField(verbose_name=b'Date')),
                ('customer', models.ForeignKey(to='booking_app.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='time',
            name='visit',
            field=models.ForeignKey(to='booking_app.Visit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='time',
            field=models.ForeignKey(to='booking_app.Time'),
            preserve_default=True,
        ),
    ]
