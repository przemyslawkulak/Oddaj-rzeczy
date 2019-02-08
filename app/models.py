from django.db import models

# Create your models here.
TYPE = (
    (1, "children"),
    (2, "mothers"),
    (3, "homeless"),
    (4, "old"),
    (5, "disabled")
)


class Institution(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    mission = models.TextField(null=True)
    type = models.IntegerField(choices=TYPE, default=1)


class Gift(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)
    given = models.BooleanField(default=False)
    clothes_to_us = models.IntegerField(null=True)
    clothes_useless = models.IntegerField(null=True)
    toys = models.IntegerField(null=True)
    books = models.IntegerField(null=True)
    others = models.IntegerField(null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    post_code = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=20, null=True)
    comments = models.TextField(null=True)

