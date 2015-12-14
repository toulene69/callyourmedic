# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0002_auto_20150923_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='hospital_email_id',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='hospital_phone1',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='hospital_phone2',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 10, 18, 679476, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 10, 18, 678822, tzinfo=utc)),
        ),
    ]
