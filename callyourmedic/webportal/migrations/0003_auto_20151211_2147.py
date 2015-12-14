# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webportal', '0002_auto_20151211_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webuser',
            name='usr_email',
            field=models.EmailField(max_length=254),
        ),
    ]
