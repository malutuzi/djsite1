# Generated by Django 2.0.5 on 2018-10-17 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alldata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adate', models.DateTimeField()),
                ('ajw_sign', models.IntegerField()),
                ('ajw_tarea', models.FloatField()),
                ('ajw_aarea', models.FloatField()),
                ('alj_deal', models.IntegerField()),
                ('alj_house', models.IntegerField()),
                ('alj_customer', models.IntegerField()),
                ('alj_visit', models.IntegerField()),
                ('alj_cuh_ratio', models.FloatField()),
                ('alj_vih_ratio', models.FloatField()),
            ],
        ),
    ]