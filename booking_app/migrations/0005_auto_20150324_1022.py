# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0004_auto_20150304_0858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time',
            name='description',
        ),
        migrations.AddField(
            model_name='booking',
            name='client_reminder',
            field=models.DateTimeField(null=True, choices=[(b'ten_m', b'10 minuter'), (b'thirty_m', b'30 minuter'), (b'one_h', b'1 timme'), (b'two_h', b'2 timmar'), (b'one_d', b'1 dag'), (b'two_d', b'2 dagar'), (b'one_w', b'1 vecka')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=datetime.datetime(2015, 3, 24, 9, 21, 56, 878410, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visit',
            name='visit_slug',
            field=autoslug.fields.AutoSlugField(default=datetime.datetime(2015, 3, 24, 9, 22, 5, 590427, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
