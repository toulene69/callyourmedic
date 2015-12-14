# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='org_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 5, 29, 588209, tzinfo=utc)),
        ),
    ]
