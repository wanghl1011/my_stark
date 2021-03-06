# Generated by Django 2.0 on 2018-02-06 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='部门')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='角色')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('dep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app03.Department', verbose_name='部门')),
                ('roles', models.ManyToManyField(to='app03.Role', verbose_name='角色')),
            ],
        ),
    ]
