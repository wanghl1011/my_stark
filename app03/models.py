from django.db import models

# Create your models here.


class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=32)
    choices = (
        (1,"男"),
        (2,"女")
    )
    sex = models.IntegerField(verbose_name="性别", choices=choices)

    dep = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE)
    roles = models.ManyToManyField(verbose_name="角色", to="Role")

    def __str__(self):
        return self.name


class Role(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="角色", max_length=32)

    def __str__(self):
        return self.name

class Department(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="部门", max_length=32)

    def __str__(self):
        return self.name
