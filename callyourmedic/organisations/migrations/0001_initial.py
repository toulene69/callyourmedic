# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apikey',
            fields=[
                ('apikey_id', models.AutoField(serialize=False, primary_key=True)),
                ('apikey_key', models.PositiveIntegerField()),
                ('apikey_status', models.BooleanField()),
                ('apikey_generation_date', models.DateTimeField()),
                ('apikey_termination_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('ord_id', models.AutoField(serialize=False, primary_key=True)),
                ('org_name', models.CharField(max_length=300)),
                ('org_brand', models.CharField(max_length=200)),
                ('org_identifier', models.CharField(unique=True, max_length=20)),
                ('org_emailid', models.EmailField(max_length=254)),
                ('org_phone', models.PositiveIntegerField()),
                ('org_active', models.CharField(max_length=1, choices=[(b'A', b'Active'), (b'D', b'Dead'), (b'T', b'Test')])),
                ('org_date_joined', models.DateTimeField(default=datetime.datetime(2015, 9, 23, 20, 5, 9, 842088, tzinfo=utc))),
                ('org_date_left', models.DateTimeField(null=True)),
                ('org_billing_id', models.CharField(max_length=100)),
                ('org_address', models.ForeignKey(to='addresses.Address')),
            ],
        ),
        migrations.AddField(
            model_name='apikey',
            name='apikey_orgid',
            field=models.ForeignKey(to='organisations.Organisation'),
        ),
    ]
