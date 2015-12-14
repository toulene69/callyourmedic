# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0003_auto_20150923_2110'),
        ('organisations', '0003_auto_20150923_2110'),
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorDetails',
            fields=[
                ('info_id', models.AutoField(serialize=False, primary_key=True)),
                ('doctor_first_name', models.CharField(max_length=100)),
                ('doctor_last_name', models.CharField(max_length=100)),
                ('doctor_gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('doctor_email', models.EmailField(max_length=254)),
                ('doctor_phone1', models.PositiveIntegerField()),
                ('doctor_phone2', models.PositiveIntegerField(null=True)),
                ('doctor_qualification', models.CharField(max_length=400)),
                ('doctor_experience', models.PositiveIntegerField(default=0)),
                ('doctor_address', models.ForeignKey(to='addresses.Address')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorRegistration',
            fields=[
                ('doctor_id', models.AutoField(serialize=False, primary_key=True)),
                ('doctor_date_joined', models.DateTimeField(verbose_name=datetime.datetime(2015, 9, 23, 21, 10, 18, 680254, tzinfo=utc))),
                ('doctor_date_left', models.DateTimeField()),
                ('doctor_status', models.BooleanField()),
                ('doctor_department', models.ForeignKey(to='hospitals.Department')),
                ('doctor_hospital_id', models.ForeignKey(to='hospitals.Hospital')),
                ('doctor_org_id', models.ForeignKey(to='organisations.Organisation')),
            ],
        ),
        migrations.AddField(
            model_name='doctordetails',
            name='doctor_id',
            field=models.ForeignKey(to='doctors.DoctorRegistration'),
        ),
    ]
