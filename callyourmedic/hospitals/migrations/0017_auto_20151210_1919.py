# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0016_auto_20151208_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 19, 19, 32, 430368, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 19, 19, 32, 429721, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_status',
            field=models.BooleanField(default=True),
        ),
    ]
