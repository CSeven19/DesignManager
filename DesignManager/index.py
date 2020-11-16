import datetime
import re
import os
import pymysql
from django.shortcuts import render, redirect
from tyOTUI.update import Config


def init(request):
    context = {}
    return render(request, 'index.html', context)


# 迭代寻找最大版本号
def getMaxVersion(versions, result):
    templist = []
    templist2 = []
    for item in versions:
        templist.append(int(item.split(".")[0]))
    for item in versions:
        if len(item.split(".")) == 1:
            result.append(max(templist))
            return result
        else:
            if int(item.split(".")[0]) == max(templist):
                str = ""
                for i in range(len(item.split(".")) - 1):
                    if i < len(item.split(".")) - 2:
                        str += item.split(".")[i + 1] + "."
                    else:
                        str += item.split(".")[i + 1]
                templist2.append(str)
    result.append(max(templist))
    getMaxVersion(templist2, result)