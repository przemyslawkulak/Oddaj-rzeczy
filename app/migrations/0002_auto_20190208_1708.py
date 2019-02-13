# Generated by Django 2.1.5 on 2019-02-08 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='books',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='clothes_to_us',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='clothes_useless',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='comments',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='others',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='post_code',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='street',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gift',
            name='toys',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='mission',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(1, 'children'), (2, 'mothers'), (3, 'homeless'), (4, 'old'), (5, 'disabled')], default=1),
        ),
    ]