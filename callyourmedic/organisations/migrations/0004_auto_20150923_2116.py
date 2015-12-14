# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0003_auto_20150923_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apikey',
            old_name='apikey_orgid',
            new_name='apikey_org',
        ),
        migrations.AlterField(
            model_name='organisation',
            name='org_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 16, 23, 124578, tzinfo=utc)),
        ),
    ]
