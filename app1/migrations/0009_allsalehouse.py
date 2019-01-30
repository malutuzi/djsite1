# Generated by Django 2.0.5 on 2018-11-21 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_delete_allsalehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allsalehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hid', models.CharField(max_length=20)),
                ('district', models.CharField(max_length=30)),
                ('str_his', models.CharField(max_length=300)),
                ('times', models.IntegerField()),
                ('price', models.CharField(max_length=15)),
                ('unitprice', models.CharField(max_length=15)),
                ('shequ_name', models.CharField(max_length=40)),
                ('shape', models.CharField(max_length=10)),
                ('square', models.CharField(max_length=10)),
                ('ori', models.CharField(max_length=10)),
                ('deco', models.CharField(max_length=10)),
                ('ele', models.CharField(max_length=5)),
                ('floor', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=5)),
                ('biz', models.CharField(max_length=10)),
                ('hur', models.CharField(max_length=100)),
                ('isSold', models.BooleanField(default=False)),
                ('isDelete', models.BooleanField(default=False)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('modifyTime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
