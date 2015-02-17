# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0002_auto_20150216_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='client_lastname',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
