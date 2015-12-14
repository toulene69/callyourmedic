# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cymportal', '0003_group_grp_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usr_last_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='usr_password',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='usr_phone',
            field=models.CharField(max_length=11, blank=True),
        ),
    ]
