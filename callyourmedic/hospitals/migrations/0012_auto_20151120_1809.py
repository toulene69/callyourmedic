# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0011_auto_20151120_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 18, 9, 51, 593777, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 18, 9, 51, 593139, tzinfo=utc)),
        ),
    ]
