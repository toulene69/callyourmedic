from __future__ import unicode_literals

from django.db import models
from hospitals.models import Department

DEPARTMENT_BASE_URL = 'https://s3-ap-southeast-1.amazonaws.com/callyourmedic-branding-resources/departments/'

# Create your models here.
class BaseBranding(models.Model):
    id = models.AutoField(primary_key=True)
    disk_name = models.CharField(max_length=100)
    actual_name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class DeptBranding(BaseBranding):
    department = models.ForeignKey(Department)

    def get_img_url(self):
        if self.disk_name is not None:
            return DEPARTMENT_BASE_URL + self.disk_name
        else:
            return None

