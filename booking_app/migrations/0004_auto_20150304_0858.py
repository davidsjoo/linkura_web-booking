# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0003_auto_20150216_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 4, 7, 58, 23, 12000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='client_mail',
            field=models.EmailField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking',
            name='client_phone',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visit',
            name='visit_date',
            field=models.DateField(verbose_name=b'Date'),
            preserve_default=True,
        ),
    ]
