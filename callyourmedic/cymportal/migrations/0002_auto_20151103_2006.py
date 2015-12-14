# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cymportal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usr_phone',
            field=models.CharField(max_length=11),
        ),
    ]
