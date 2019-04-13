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
    city = models.CharField(max_length=255, null=True)
    mission = models.TextField(null=True)
    type = models.IntegerField(choices=TYPE, default=1)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.address} {self.city} {self.mission} {self.type} '


class Gift(models.Model):
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    given = models.BooleanField(default=False)
    clothes_to_use = models.IntegerField(null=True)
    clothes_useless = models.IntegerField(null=True)
    toys = models.IntegerField(null=True)
    books = models.IntegerField(null=True)
    others = models.IntegerField(null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    post_code = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=10, null=True)
    comments = models.TextField(null=True)

    def __str__(self):
        return f'{self.date} {self.given} {self.clothes_to_use} {self.clothes_useless} {self.toys} ' \
            f'{self.books} {self.others}'
