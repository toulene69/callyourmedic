# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0004_auto_20150923_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 18, 42, 790733, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 18, 42, 790083, tzinfo=utc)),
        ),
    ]
