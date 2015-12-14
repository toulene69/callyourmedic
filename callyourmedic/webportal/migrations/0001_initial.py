# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0015_auto_20151124_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebGroup',
            fields=[
                ('grp_id', models.AutoField(serialize=False, primary_key=True)),
                ('grp_name', models.CharField(max_length=50)),
                ('grp_org', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_hospital', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_doctor', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_patients', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_call', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_transaction', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_user', models.PositiveIntegerField(choices=[(0, b'No Access'), (1, b'Read Only'), (2, b'Read Write')])),
                ('grp_org_id', models.ForeignKey(to='organisations.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='WebUser',
            fields=[
                ('usr_id', models.AutoField(serialize=False, primary_key=True)),
                ('usr_first_name', models.CharField(max_length=100)),
                ('usr_last_name', models.CharField(max_length=100, blank=True)),
                ('usr_email', models.EmailField(unique=True, max_length=254)),
                ('usr_phone', models.CharField(max_length=11, blank=True)),
                ('usr_password', models.CharField(max_length=20, blank=True)),
                ('usr_group', models.ForeignKey(to='webportal.WebGroup')),
                ('usr_org', models.ForeignKey(to='organisations.Organisation')),
            ],
        ),
    ]
