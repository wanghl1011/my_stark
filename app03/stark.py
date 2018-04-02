from stark.server import stark
from app03.models import *
# print("app02")


class UserStark(stark.ModelStark):
    search_fields = ["name", ]
    edit_link = ["name",]
    def display_department(self,obj=None,is_head=False):
        if is_head:
            return "部门"
        else:
            return obj.dep.name

    def display_roles(self,obj=None,is_head=False):
        if is_head:
            return "角色"
        else:
            role_list=obj.roles.all()
            temp=[]
            for obj in role_list:
                temp.append(obj.name)

            return ",".join(temp)

    def display_gender(self,obj=None, is_head=False):
        if is_head:
            return "性别"
        else:
            return obj.get_sex_display()

    list_display = ["name", display_gender, display_department, display_roles]




    group_filter = [
         stark.FilterOption("sex", is_choice=True),
         stark.FilterOption("dep"),
         stark.FilterOption("roles", is_multi=True),
    ]



stark.site.register(UserInfo,UserStark)
stark.site.register(Role)
stark.site.register(Department)
