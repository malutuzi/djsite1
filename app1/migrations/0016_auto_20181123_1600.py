# Generated by Django 2.0.5 on 2018-11-23 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_auto_20181123_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='alldata',
            name='backup1',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='alldata',
            name='backup2',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='alldata',
            name='dayd',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='alldata',
            name='dayu',
            field=models.IntegerField(default=None),
        ),
    ]
