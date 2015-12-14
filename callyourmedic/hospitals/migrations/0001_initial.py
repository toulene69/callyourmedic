# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(serialize=False, primary_key=True)),
                ('department_name', models.CharField(max_length=100)),
                ('department_code', models.CharField(max_length=10)),
                ('department_status', models.BooleanField(default=True)),
                ('department_date_added', models.DateTimeField(default=datetime.datetime(2015, 9, 23, 20, 5, 9, 844143, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('hospital_id', models.AutoField(serialize=False, primary_key=True)),
                ('hospital_name', models.CharField(max_length=200)),
                ('hospital_branch_code', models.CharField(max_length=50)),
                ('hospital_status', models.BooleanField()),
                ('hospital_date_joined', models.DateTimeField(default=datetime.datetime(2015, 9, 23, 20, 5, 9, 843534, tzinfo=utc))),
                ('hospital_date_left', models.DateTimeField()),
                ('hospital_address', models.ForeignKey(to='addresses.Address')),
                ('hospital_org_id', models.ForeignKey(to='organisations.Organisation')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='department_hospital_id',
            field=models.ForeignKey(to='hospitals.Hospital'),
        ),
        migrations.AddField(
            model_name='department',
            name='department_org_id',
            field=models.ForeignKey(to='organisations.Organisation'),
        ),
    ]
