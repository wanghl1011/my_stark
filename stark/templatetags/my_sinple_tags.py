import unittest
from django.urls import reverse
from django.forms.models import ModelChoiceField
from django import template
# 必须叫register
register = template.Library()
# 引入装饰器，filter就是过滤器
@register.filter
def cheng(a,b):
    # 参数a就代表被渲染的模版变量，b就代表冒号后跟着的参数
    return a*b


@register.inclusion_tag("form_show.html")
def get_form_info(form):
    form_info = []
    for field in form:
        # print(field,"%r"%field)
        if isinstance(field.field, ModelChoiceField):
            # 当前字段对象对应的model类
            field_model = field.field.queryset.model
            # 对应的model类的app名
            _app_label = field_model._meta.app_label
            # 对应的model类的名字
            _model_name = field_model._meta.model_name
            pop_up_id = field.auto_id
            name = "stark:%s_%s_add" % (_app_label, _model_name)
            _url = reverse(name)
            fina_url = "%s?pop_up_id=%s" % (_url, pop_up_id)
            form_info.append({"form": field, "is_pop_up": True, "url": fina_url})
        else:
            form_info.append({"form": field, "is_pop_up": False})
    return {"form_info":form_info}