# -*- coding = utf-8 -*-
# @Time: 2022/05/22 17:37
# @Author: ChengXing
# @Software: Pycharm

from django.http import HttpResponseRedirect

def hello(request):
    return HttpResponseRedirect('/home/')