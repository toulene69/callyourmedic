# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0019_auto_20151211_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='org_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 21, 14, 21, 126708, tzinfo=utc)),
        ),
    ]
