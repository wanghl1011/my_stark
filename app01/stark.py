# print("app01")

from stark.server import stark
from app01.models import *
from django.utils.safestring import mark_safe
from django.forms import ModelForm,widgets


class BooKModelForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "pub_date": widgets.TextInput(attrs={"type": "date"})
        }


class BookStark(stark.ModelStark):
    list_display=('title', "price","publish")
    model_form_class = BooKModelForm
    search_fields = ["title", "price"]

    def patch_init(self, request, queryset):
        queryset.update(price=0)

    patch_init.short_desc = "批量价格初始化"

    actions = [patch_init, ]

    group_filter = [
        stark.FilterOption("publish",),
        stark.FilterOption("writer",is_multi=True)
    ]


class PublishStark(stark.ModelStark):
    list_display = ("pname",)


class WriterStark(stark.ModelStark):
    list_display = ("wname",)

stark.site.register(Book, BookStark)
stark.site.register(Publish, PublishStark)
stark.site.register(Writer, WriterStark)
