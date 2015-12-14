# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webportal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webgroup',
            name='grp_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='webuser',
            name='usr_status',
            field=models.BooleanField(default=True),
        ),
    ]
