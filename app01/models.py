from django.db import models

# Create your models here.
class Book(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(verbose_name="书名", max_length=32)
    pub_date=models.DateField()
    price=models.DecimalField(verbose_name="价格", max_digits=5, decimal_places=2)

    publish = models.ForeignKey(verbose_name="出版社", to="Publish", on_delete=models.CASCADE, default=1)
    writer = models.ManyToManyField(verbose_name="作者", to="Writer")

    def __str__(self):
        return self.title

class Publish(models.Model):
    nid=models.AutoField(primary_key=True)
    pname=models.CharField(verbose_name="出版社名称",max_length=32)

    def __str__(self):
        return self.pname

class Writer(models.Model):
    nid = models.AutoField(primary_key=True)
    wname=models.CharField(verbose_name="姓名", max_length=32)

    def __str__(self):
        return self.wname
