# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0013_auto_20151123_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organisation',
            old_name='ord_id',
            new_name='org_id',
        ),
        migrations.AlterField(
            model_name='organisation',
            name='org_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 23, 18, 38, 22, 403730, tzinfo=utc)),
        ),
    ]
