# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0009_auto_20151120_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorregistration',
            name='doctor_date_joined',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 11, 20, 18, 9, 51, 594472, tzinfo=utc)),
        ),
    ]
