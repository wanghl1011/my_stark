# Generated by Django 2.0 on 2018-01-26 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20180126_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pub_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='publish',
            name='pname',
            field=models.CharField(max_length=32, verbose_name='出版社名称'),
        ),
        migrations.AlterField(
            model_name='writer',
            name='wname',
            field=models.CharField(max_length=32, verbose_name='姓名'),
        ),
    ]
