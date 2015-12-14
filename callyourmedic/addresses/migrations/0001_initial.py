# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(serialize=False, primary_key=True)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100)),
                ('address_city', models.CharField(max_length=100)),
                ('address_state', models.CharField(max_length=2, choices=[(b'AN', b'Andaman and Nicobar Islands '), (b'AP', b'Andhra Pradesh'), (b'AR', b'Arunachal Pradesh'), (b'AS', b'Assam'), (b'BR', b'Bihar'), (b'CG', b'Chhattisgarh'), (b'DL', b'New Delhi'), (b'GA', b'Goa'), (b'GJ', b'Gujarat'), (b'HR', b'Haryana'), (b'HP', b'Himachal Pradesh'), (b'JK', b'Jammu and Kashmir'), (b'JH', b'Jharkhand'), (b'KA', b'Karnataka'), (b'KL', b'Kerela'), (b'LD', b'Lakshadweep'), (b'MP', b'Madhya Pradesh'), (b'MH', b'Maharashtra'), (b'MN', b'Manipur'), (b'ML', b'Meghalaya'), (b'MZ', b'Mizoram'), (b'NL', b'Nagaland'), (b'OR', b'Odisha'), (b'PY', b'Puducherry'), (b'PB', b'Punjab'), (b'RJ', b'Rajasthan'), (b'SK', b'Sikkim'), (b'TN', b'Tamil Nadu'), (b'TL', b'Telangana'), (b'TR', b'Tripura'), (b'UP', b'Uttar Pradesh'), (b'UK', b'Uttarakhand'), (b'WB', b'West Bengal')])),
                ('address_pincode', models.PositiveIntegerField()),
                ('address_status', models.BooleanField(default=True)),
            ],
        ),
    ]
