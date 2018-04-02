import copy
class Page:
    def __init__(self, all_info_count, current_page, page_url, params, page_info_count=10, page_count=11):
        self.all_info_count = all_info_count
        self.page_url = page_url
        self.page_info_count = page_info_count
        self.page_count = page_count
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page <= 0:
            current_page = 1
        self.current_page = current_page
        """
            封装分页相关数据
            :param current_page: 当前页
            :param all_info_count:  数据库中的数据总条数
            :param page_info_count: 每页显示的数据条数
            :param page_url: 分页中显示的URL前缀
            :param page_count:  最多显示的页码个数
            :param params:  分页的URL中的GET数据
        """
        total_page, yushu = divmod(self.all_info_count, self.page_info_count)
        if yushu:
            total_page += 1

        # 总页码数
        self.total_page = total_page
        # 最多显示页码个数的一半
        self.page_count_half = int((self.page_count - 1) / 2)

        # params = request.GET
        param=copy.deepcopy(params)
        param._mutable=True
        # 深拷贝GET数据后得到的一个Querydict类型，用于生成动态的页码标签href属性，要保持URL的数据状态不变，只有页码参数变化
        self.param = param

    @property
    def start(self):
        return (self.current_page - 1) * self.page_info_count

    @property
    def end(self):
        return self.current_page * self.page_info_count

    def page_http(self):
        # 如果计算出的总页码数小于规定的每页的页码数
        if self.total_page <= self.page_count:
            page_start = 1
            page_end = self.total_page
        # 总页码大于规定的每页页码数
        else:
            page_start = self.current_page - self.page_count_half
            page_end = self.current_page + self.page_count_half
            # 起始页码小于0的处理
            if page_start <= 0:
                page_start = 1
                page_end = self.page_count
                # 最终页码大于总页码的处理
            if page_end > self.total_page:
                page_end = self.total_page
                page_start = self.total_page - self.page_count + 1



        page_list = []
        self.param["_page"] = 1
        page_list.append("<li><a href='%s?%s'>首页</a></li>"%(self.page_url,self.param.urlencode()))
        if self.current_page == 1:
            page_list.append("<li class='disabled'><a href='%s?%s'>上一页</a></li>"%(self.page_url,self.param.urlencode()))
        else:
            self.param["_page"] = self.current_page - 1
            page_list.append("<li><a href='%s?%s'>上一页</a></li>" % (self.page_url,self.param.urlencode()))
        for i in range(page_start, page_end + 1):
            self.param["_page"] = i
            if i == self.current_page:
                page_list.append("<li class='active'><a href='%s?%s'>%s</a></li>" % (self.page_url,self.param.urlencode(), i))
            else:
                page_list.append("<li><a href='%s?%s'>%s</a></li>" % (self.page_url,self.param.urlencode(),i))
        if self.current_page == self.total_page:
            self.param["_page"] = self.total_page
            page_list.append("<li class='disabled'><a href='%s?%s'>下一页</a></li>" % (self.page_url,self.param.urlencode()))
        else:
            self.param["_page"] = self.current_page + 1
            page_list.append("<li><a href='%s?%s'>下一页</a></li>" % (self.page_url,self.param.urlencode(),))
        self.param["_page"] = self.total_page
        page_list.append("<li><a href='%s?%s'>尾页</a></li>" % (self.page_url,self.param.urlencode(),))
        page = ''.join(page_list)
        return page
