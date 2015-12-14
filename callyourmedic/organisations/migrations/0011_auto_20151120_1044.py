# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0010_auto_20151103_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='org_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 10, 44, 29, 687453, tzinfo=utc)),
        ),
    ]
