# Generated by Django 2.0.5 on 2018-11-22 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_alldealhouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='alldata',
            name='snumber',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
