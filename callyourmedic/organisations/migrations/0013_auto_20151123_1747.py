# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0012_auto_20151120_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='org_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 23, 17, 47, 24, 390023, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='org_phone',
            field=models.CharField(max_length=11, blank=True),
        ),
    ]
