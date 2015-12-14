# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_auto_20150923_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetails',
            name='doctor_id',
            field=models.ForeignKey(to='doctors.DoctorRegistration', db_column=b'doctor_id'),
        ),
        migrations.AlterField(
            model_name='doctorregistration',
            name='doctor_date_joined',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 9, 23, 21, 18, 42, 792613, tzinfo=utc)),
        ),
    ]
