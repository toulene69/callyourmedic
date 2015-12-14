# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0013_auto_20151124_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorregistration',
            name='doctor_date_joined',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 12, 8, 19, 16, 15, 417306, tzinfo=utc)),
        ),
    ]
