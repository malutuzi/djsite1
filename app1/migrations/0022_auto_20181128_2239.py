# Generated by Django 2.0.5 on 2018-11-28 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_allljshequ_trend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allljshequ',
            name='trend',
            field=models.CharField(default='', max_length=10),
        ),
    ]