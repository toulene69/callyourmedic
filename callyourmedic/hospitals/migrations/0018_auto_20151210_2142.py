# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0017_auto_20151210_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 21, 42, 44, 229271, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 21, 42, 44, 228580, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_left',
            field=models.DateTimeField(null=True),
        ),
    ]
