# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='time',
            options={'ordering': ['datetime']},
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='client_name',
            new_name='client_firstname',
        ),
        migrations.AddField(
            model_name='booking',
            name='client_lastname',
            field=models.CharField(default=b'Andersson', max_length=50),
            preserve_default=True,
        ),
    ]
