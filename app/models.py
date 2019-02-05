from django.db import models


# Create your models here.

class Institution(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Gift(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)
    given = models.BooleanField(default=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
