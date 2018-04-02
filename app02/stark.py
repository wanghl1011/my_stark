from stark.server import stark
from app02.models import *
# print("app02")


class AuthorStark(stark.ModelStark):
    list_display = ('name', "age")

stark.site.register(Author, AuthorStark)
