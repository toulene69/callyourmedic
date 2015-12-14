# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_auto_20151103_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorregistration',
            name='doctor_date_joined',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 11, 20, 10, 44, 29, 690220, tzinfo=utc)),
        ),
    ]
