# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorregistration',
            old_name='doctor_hospital_id',
            new_name='doctor_hospital',
        ),
        migrations.RenameField(
            model_name='doctorregistration',
            old_name='doctor_org_id',
            new_name='doctor_org',
        ),
        migrations.AlterField(
            model_name='doctorregistration',
            name='doctor_date_joined',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 9, 23, 21, 16, 23, 128422, tzinfo=utc)),
        ),
    ]
