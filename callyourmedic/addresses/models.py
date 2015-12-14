from django.db import models

class Address(models.Model):
    ADDRESS_STATES = (
        ('AN','Andaman and Nicobar Islands '),
        ('AP','Andhra Pradesh'),
        ('AR','Arunachal Pradesh'),
        ('AS','Assam'),
        ('BR','Bihar'),
        ('CG','Chhattisgarh'),
        ('DL','New Delhi'),
        ('GA','Goa'),
        ('GJ','Gujarat'),
        ('HR','Haryana'),
        ('HP','Himachal Pradesh'),
        ('JK','Jammu and Kashmir'),
        ('JH','Jharkhand'),
        ('KA','Karnataka'),
        ('KL','Kerela'),
        ('LD','Lakshadweep'),
        ('MP','Madhya Pradesh'),
        ('MH','Maharashtra'),
        ('MN','Manipur'),
        ('ML','Meghalaya'),
        ('MZ','Mizoram'),
        ('NL','Nagaland'),
        ('OR','Odisha'),
        ('PY','Puducherry'),
        ('PB','Punjab'),
        ('RJ','Rajasthan'),
        ('SK','Sikkim'),
        ('TN','Tamil Nadu'),
        ('TL','Telangana'),
        ('TR','Tripura'),
        ('UP','Uttar Pradesh'),
        ('UK','Uttarakhand'),
        ('WB','West Bengal'),
    )

    address_id         = models.AutoField(primary_key=True)
    address_line1      = models.CharField(max_length=100)
    address_line2      = models.CharField(max_length=100)
    address_city       = models.CharField(max_length=100)
    address_state      = models.CharField(max_length=2, choices = ADDRESS_STATES)
    address_pincode    = models.PositiveIntegerField()
    address_status     = models.BooleanField(default=True)
