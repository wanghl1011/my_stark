# Generated by Django 2.0 on 2018-01-24 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='age',
            field=models.CharField(max_length=3, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=32, verbose_name='姓名'),
        ),
    ]