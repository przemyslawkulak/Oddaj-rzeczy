# Generated by Django 2.1.5 on 2019-02-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190213_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
