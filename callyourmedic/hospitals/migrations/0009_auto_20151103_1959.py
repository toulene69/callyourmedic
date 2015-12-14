# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0008_auto_20151021_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='department_hospital',
        ),
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 19, 59, 19, 484897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 19, 59, 19, 484254, tzinfo=utc)),
        ),
    ]
