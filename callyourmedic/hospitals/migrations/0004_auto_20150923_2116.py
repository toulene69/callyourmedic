# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0003_auto_20150923_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='department_hospital_id',
            new_name='department_hospital',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='department_org_id',
            new_name='department_org',
        ),
        migrations.RenameField(
            model_name='hospital',
            old_name='hospital_org_id',
            new_name='hospital_org',
        ),
        migrations.AlterField(
            model_name='department',
            name='department_date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 16, 23, 127228, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospital_date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 23, 21, 16, 23, 126582, tzinfo=utc)),
        ),
    ]
