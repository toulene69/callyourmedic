# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0018_auto_20151210_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='department_description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 20, 9, 42, 88861, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 20, 9, 42, 88167, tzinfo=utc)),
        ),
    ]
