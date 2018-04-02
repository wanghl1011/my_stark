from django.contrib import admin
from app01.models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display=('title',"price","pub_date","publish",)

admin.site.register(Book,BookAdmin)
admin.site.register(Publish)
admin.site.register(Writer)