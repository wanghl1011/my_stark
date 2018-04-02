from django.conf.urls import url
from django.urls import path
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
from stark.my_page import Page
from django.http import QueryDict,JsonResponse
import json
from django.db.models import Q, ForeignKey, ManyToManyField
from app03.models import UserInfo,Department,Role
import copy
from django.forms import TypedChoiceField, TypedMultipleChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.boundfield import BoundField


# 代表某一个字段对象
# 为FilterRow服务
class FilterOption:
    def __init__(self,field_name, is_multi=False, is_choice=False):
        self.field_name = field_name
        self.is_choice = is_choice
        self.is_multi = is_multi

    def get_queryset(self,field_obj):
        return field_obj.related_model.objects.all()

    def get_choices(self,field_obj):
        return field_obj.choices


# 渲染出某个字段对象对应的所有数据，在模版中以一行显示，所以命名为ROW
# 为ModelList服务
class FilterRow:
    def __init__(self,data,option_obj,request):
        self.data = data
        self.filter_option_obj = option_obj
        self.request = request
    def __iter__(self):
        field_name =self.filter_option_obj.field_name
        params = copy.deepcopy(self.request.GET)
        current_id = self.request.GET.get(field_name)
        current_id_list = self.request.GET.getlist(field_name,[])
        # 处理全部a标签
        if params.get(field_name):
            del params[field_name]
            _url="%s?%s"%(self.request.path,params.urlencode())
            all_html = "<a href='%s'>全部</a>"%_url
        else:
            _url = "%s?%s" % (self.request.path, params.urlencode())
            all_html = "<a class='active' href='%s'>全部</a>" % _url
        yield mark_safe(all_html)

        # 处理具体的model对象a标签
        for field_model in self.data:
            if self.filter_option_obj.is_choice:
                pk, text = str(field_model[0]), field_model[1]
            else:
                pk, text = str(field_model.pk), str(field_model)

            path = self.request.path

            params[field_name] = pk
            if not self.filter_option_obj.is_multi:
                _url = "%s?%s"%(path, params.urlencode())


                if current_id==pk:
                    field_model_html = "<a class='active' href='%s'>%s</a>"%(_url,text)
                else:
                    field_model_html = "<a href='%s'>%s</a>" % (_url, text)
                yield mark_safe(field_model_html)
            else:
                _params = copy.deepcopy(self.request.GET)
                # 多对多字段的数据

                if pk in current_id_list:
                    _url = "%s?%s" % (path, _params.urlencode())
                    field_model_html = "<a class='active' href='%s'>%s</a>" % (_url, text)
                    yield mark_safe(field_model_html)
                else:
                    data_list = _params.getlist(field_name,[])
                    data_list.append(pk)
                    _params.setlist(field_name, data_list)
                    _url = "%s?%s" % (path, _params.urlencode())
                    field_model_html = "<a href='%s'>%s</a>" % (_url, text)
                    yield mark_safe(field_model_html)


# 为ModelStark服务
class ModelList:
    def __init__(self, model_stark_obj, queryset):
        self.model_stark_obj = model_stark_obj
        self.queryset = queryset

        # 数据总量
        all_info_count = self.queryset.count()
        # 当前页
        current_page = self.model_stark_obj.request.GET.get(self.model_stark_obj.page_key)
        # 分页显示的URL前缀
        page_url = self.model_stark_obj.request.path_info
        # 用于保存URL中的数据状态
        params = self.model_stark_obj.request.GET
        # 每页显示数据个数
        page_info_count = 5
        # 每页显示页码个数
        page_count = 5
        page = Page(all_info_count, current_page, page_url, params, page_info_count, page_count)

        self.page = page

        # 模糊查询
        self.search_fields = self.model_stark_obj.search_fields
        self.request = self.model_stark_obj.request

        self.search_key = self.model_stark_obj.search_key
        self.search_val = self.request.GET.get(self.search_key, "")
        # 批量操作
        self.actions = self.model_stark_obj.get_actions

        # 组合查询
        self.group_filter = self.model_stark_obj.group_filter

    # 表头
    @property
    def get_head(self):
        head_list = []
        if not self.model_stark_obj.list_display:
            head_list = [mark_safe("<input class='total-check' type='checkbox'>"),self.model_stark_obj.model._meta.model_name, "操作", "操作"]
        else:
            for field_name in self.model_stark_obj.get_list_display():
                if isinstance(field_name, str):
                    verbose_name = self.model_stark_obj.model._meta.get_field(field_name).verbose_name
                else:
                    verbose_name = field_name(self.model_stark_obj,is_head=True)
                head_list.append(verbose_name)
            # head_list.insert(1,"ID")

        return head_list

    # 数据
    @property
    def get_data(self):

        model_list = self.queryset
        data_list = []
        for model in model_list:
            temp = []
            if not self.model_stark_obj.list_display:
                temp.append(ModelStark.checkbox(self.model_stark_obj,model,))
                temp.append(model)
                temp.append(ModelStark.modify(self.model_stark_obj,model,))
                temp.append(ModelStark.dele(self.model_stark_obj,model,))
            else:
                for field_name in self.model_stark_obj.get_list_display():
                    if isinstance(field_name, str):
                        val = getattr(model, field_name)
                        if field_name in self.model_stark_obj.edit_link:
                            val = self.get_edit_link_tag(model,val)
                    else:
                        # print(field_name)
                        val = field_name(self.model_stark_obj,model)
                        # print(val)
                    temp.append(val)
                # temp.insert(1,model.pk)
            data_list.append(temp)
        new_data_list = data_list[self.page.start:self.page.end]
        return new_data_list

    # 得到编辑标签
    def get_edit_link_tag(self, obj,val):
        edit_url = self.model_stark_obj.get_edit_url(obj)
        q = QueryDict()
        q._mutable = True
        if not self.request.GET:
            q["_page"] = 1
        else:
            q["_listfilter"] = self.request.GET.urlencode()
        new_edit_url = edit_url + "?%s" % q.urlencode()
        return mark_safe("<a href='" + new_edit_url + "'>"+val+"</a>")

    # 模糊查询
    def handle_actions(self):
        ret = []
        # print(1111111, self.actions)
        for func in self.actions:
            ret.append({"name": func.__name__, "desc": func.short_desc})

        return ret

    # 组合查询
    def get_group_filter(self):
        if self.group_filter:
            for filter_option_obj in self.group_filter:
                field_obj = self.model_stark_obj.model._meta.get_field(filter_option_obj.field_name)
                if isinstance(field_obj,ForeignKey) or isinstance(field_obj,ManyToManyField):
                    filter_row_obj = FilterRow(filter_option_obj.get_queryset(field_obj),filter_option_obj,self.request)
                else:
                    filter_row_obj = FilterRow(filter_option_obj.get_choices(field_obj),filter_option_obj,self.request)
                yield filter_row_obj


class ModelStark:
    """
    样式类
    """
    list_display = ()
    search_fields = []
    actions = []
    group_filter = []
    edit_link = []
    def __init__(self, model, site):
        # model对应的类对象，就是model中定义的类
        self.model = model
        # StarkSite对象
        self.site = site
        self.request = None
        self.search_key = 'q'
        self.page_key = '_page'

    def get_add_url(self):
        url = 'stark:%s_%s_add' % (self.model._meta.app_label, self.model._meta.model_name)
        add_url = reverse(url,)
        # print("edit_url",edit_url)
        q = QueryDict()
        q._mutable = True
        q["_listfilter"] = self.request.GET.urlencode()
        new_edit_url = add_url + "?%s" % q.urlencode()
        return new_edit_url

    def get_edit_url(self, obj):
        url = 'stark:%s_%s_edit' % (self.model._meta.app_label, self.model._meta.model_name)
        edit_url = reverse(url, args=(obj.nid,))
        # print("edit_url",edit_url)
        return edit_url

    def get_del_url(self, obj):
        url = 'stark:%s_%s_del' % (self.model._meta.app_label, self.model._meta.model_name)
        del_url = reverse(url, args=(obj.nid,))
        return del_url

    def get_list_url(self):
        url = 'stark:%s_%s_model_list' % (self.model._meta.app_label, self.model._meta.model_name)
        list_url = reverse(url, )
        return list_url

    def get_list_display(self):
        default_list_display = []
        if self.list_display:
            default_list_display.extend(self.list_display)
            default_list_display.insert(0, ModelStark.checkbox)
            if not self.edit_link:
                default_list_display.append(ModelStark.modify)
            default_list_display.append(ModelStark.dele)
        return default_list_display

    def wrapper(self,func):
        def inner(request,*args,**kwargs):
            self.request=request
            ret = func(request, *args, **kwargs)
            return ret
        return inner

    # 编辑样式
    def modify(self, obj=None, is_head=False):
        if obj:
            edit_url = self.get_edit_url(obj)
            # current_page = self.get_page_obj(request).current_page
            # edit_url=edit_url+"?page=%s"%current_page
            # edit_url=request.get_full_path()
            q = QueryDict()
            q._mutable=True
            if not self.request.GET:
                q["_page"] = 1
            else:
                q["_listfilter"] = self.request.GET.urlencode()
            new_edit_url = edit_url + "?%s" % q.urlencode()
            # print(new_edit_url)
            return mark_safe("<a href='" + new_edit_url + "'>编辑</a>")
        if is_head:
            return "操作"

    # 删除样式
    def dele(self, obj=None, is_head=False):
        if obj:
            del_url=self.get_del_url(obj)
            # q = QueryDict()
            # q._mutable = True
            # q["_listfilter"] = self.request.GET.urlencode()
            new_del_url = del_url + "?%s" % self.request.GET.urlencode()
            return mark_safe("<a href='" + new_del_url + "'>删除</a>")
        if is_head:
            return "操作"

    # 多选样式
    def checkbox(self, obj=None, is_head=False):
        if is_head:
            return mark_safe("<input class='total-check' type='checkbox'>")
        return mark_safe("<input class='checkbox' name='pk' value=%s type='checkbox'>"%obj.pk)

    def get_search_condition(self):
        keyword = self.request.GET.get(self.search_key,"")
        condition = Q()
        if keyword:
            condition.connector = "or"
            for item in self.search_fields:
                condition.children.append((item + "__contains", keyword))
        return condition

    # 查询应用
    def model_list(self, request):
        add_url = self.get_add_url()
        list_url = self.get_list_url()
        if request.method == "POST":
            action_func_str=request.POST.get("action")
            pk_list = request.POST.getlist("pk")
            if action_func_str and pk_list:
                action_func = getattr(self,action_func_str)

                queryset=self.model.objects.filter(pk__in=pk_list)

                ret = action_func(request, queryset)
                if ret:
                    return ret

        # 模糊查询的条件
        condition = self.get_search_condition()
        print("模糊查询",condition)


        # 组合查询的条件
        params = copy.deepcopy(request.GET)
        condition_dict = {}
        flag = False
        print("request.GET",request.GET)
        for con in params.keys():
            for option_obj in self.group_filter:
                if option_obj.field_name == con:
                    flag = True
                    break
            if flag:
                condition_dict["%s__in"%con] = params.getlist(con)
        print("组合查询1",condition_dict)
        if self.page_key+"__in" in condition_dict:
            del condition_dict[self.page_key+"__in"]
        print("组合查询2", condition_dict)

        query_set = self.model.objects.filter(condition).filter(**condition_dict)
        model_list = ModelList(self, query_set)

        return render(request, 'model_list.html', locals())

    # 默认自带的批量删除函数
    def pl_delete(self, request, queryset):
        queryset.delete()
    pl_delete.short_desc = "批量删除"

    # 处理批量操作
    @property
    def get_actions(self):
        temp = []
        temp.append(self.pl_delete)
        temp.extend(self.actions)
        # print("temp", temp)

        return temp

    model_form_class = None

    def get_model_form_class(self):
        if self.model_form_class:
            model_form_class=self.model_form_class
        else:
            from django.forms import ModelForm
            class StarkModelForm(ModelForm):
                class Meta:
                    model=self.model
                    fields="__all__"

            model_form_class=StarkModelForm
        return model_form_class

    # 添加应用
    def add(self, request):
        model_form_class = self.get_model_form_class()
        model_name = self.model._meta.model_name
        # print("_________",model_name)
        app_label = self.model._meta.app_label
        if request.method=='POST':
            form = model_form_class(data=request.POST)
            if form.is_valid():
                print("is_valid")
                model_obj = form.save()
                pop_up_id = request.GET.get("pop_up_id")
                if pop_up_id:
                    print("121212121212",pop_up_id)
                    ret={"pop_up_id":pop_up_id,"model_pk":str(model_obj.pk),"model_name":str(model_obj)}
                    data_dict = {"ret":json.dumps(ret)}

                    return render(request,"pop_post.html",{"data":json.dumps(ret)})

                list_url=self.get_list_url()
                redirect_url=list_url+"?%s"%request.GET.get("_listfilter", "")
                return redirect(redirect_url)
            else:
                return render(request,'model_add.html',locals())
        else:
            form = model_form_class()
            a = 100
            return render(request,'model_add.html',locals())

    # 编辑应用
    def edit(self, request, id):
        edit_model = self.model.objects.filter(pk=id).first()
        if not edit_model:
            return redirect(self.get_list_url())
        model_form_class = self.get_model_form_class()
        model_name = self.model._meta.model_name
        if request.method == 'POST':
            # print("path", request.GET.get("page"))
            form = model_form_class(data=request.POST, instance=edit_model)
            if form.is_valid():
                form.save()
                # current_page = self.get_page_obj(request).current_page
                # redirect_url=self.get_list_url()+"?page=%s"%current_page
                data=request.GET.get("_listfilter")
                print("data",data)
                redirect_url = self.get_list_url() + "?%s" % data
                return redirect(redirect_url)
            else:
                return render(request, 'model_edit.html', locals())
        else:
            # print("path",request.get_full_path())
            form = model_form_class(instance=edit_model)
            return render(request, 'model_edit.html', locals())

    # 删除应用
    def delete(self, request, id):
        model_name=self.model._meta.model_name
        if request.method=='POST':
            self.model.objects.filter(pk=id).delete()

            list_url = self.get_list_url()
            # model_list = ModelList(self)
            # if request.GET.get("_page") > model_list.page.total_page:
            #     pass
            redirect_url = list_url+"?%s"%request.GET.urlencode()

            return redirect(list_url)
        else:
            return render(request,'model_del.html',locals())

    @property
    def urls(self):
        return self.get_urls()   # stark是namespace参数值，就是名称空间

    def get_urls(self):
        app_model_name = (self.model._meta.app_label, self.model._meta.model_name)
        # print("app_model_name",app_model_name)
        url_temp=[
            # path('', self.model_list,name="%s_%s_model_list"%app_model_name),
            # path('add/', self.add, name="%s_%s_add"%app_model_name),
            # path('<int:id>/edit/', self.edit, name="%s_%s_edit"%app_model_name),
            # path('<int:id>/del/', self.delete, name="%s_%s_del"%app_model_name),
            url('^$', self.wrapper(self.model_list), name="%s_%s_model_list" % app_model_name),
            url('^add/$', self.wrapper(self.add), name="%s_%s_add" % app_model_name),
            url(r'^(\d+)/edit/$', self.wrapper(self.edit), name="%s_%s_edit" % app_model_name),
            url(r'^(\d+)/del/$', self.wrapper(self.delete), name="%s_%s_del" % app_model_name),
        ]
        return url_temp


class StarkSite:
    """
    应用类
    """
    def __init__(self):
        self._registry = {}

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelStark
        self._registry[model] = stark_class(model, self)

    @property
    def urls(self):
        return self.get_urls(), 'stark', 'stark'

    def get_app_dict(self):
        index_dict = {}
        for model in self._registry:
            app_label = model._meta.app_label
            if app_label in index_dict:
                index_dict.get(app_label).append(model._meta.model_name)
            else:
                index_dict[app_label] = [model._meta.model_name]
        return index_dict

    def index(self, request):
        index_dict=self.get_app_dict()
        return render(request,'model_index.html',locals())

    def get_urls(self):
        urlpatterns=[]
        for model, stark_model in self._registry.items():
            # 所在的app文件名
            app_label = model._meta.app_label
            # model对应的类名，也就是表名
            model_name = model._meta.model_name

            # r_url = path('%s/%s/' % (app_label,model_name), stark_model.urls)
            r_url = url('^%s/%s/' % (app_label, model_name), (stark_model.urls, None, None))
            urlpatterns.append(r_url)
        # urlpatterns.append(path('', self.index))
        urlpatterns.append(url('^$', self.index))
        return urlpatterns

site = StarkSite()
