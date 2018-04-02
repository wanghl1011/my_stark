from django.db import models

# Create your models here.
class Author(models.Model):
    nid=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="姓名",max_length=32)
    age=models.CharField(verbose_name="年龄",max_length=3)

    def __str__(self):
        return self.name