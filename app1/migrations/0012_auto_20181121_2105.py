# Generated by Django 2.0.5 on 2018-11-21 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_allsalehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='allsalehouse',
            name='backup1',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='allsalehouse',
            name='backup2',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='allsalehouse',
            name='dealprice',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='allsalehouse',
            name='shequ_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]