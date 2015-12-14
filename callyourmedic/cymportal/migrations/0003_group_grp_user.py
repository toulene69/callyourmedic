# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cymportal', '0002_auto_20151103_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='grp_user',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')]),
            preserve_default=False,
        ),
    ]
