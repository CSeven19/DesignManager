import datetime
import pymysql
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from tyOTUI.update import Config


def init(request):
    context = {}
    context['userlist'] = userlist()
    return render(request, 'user.html', context)


@csrf_exempt
def usercreate(request):
    if request.method == "POST":
        name = request.POST.get("mode_createUser_name")
        olduser = selectbyname(name, "")
        if olduser is not None and len(olduser) > 0:
            return redirect('/user')
        password = request.POST.get("mode_createUser_password")
        power = request.POST.get("mode_createUser_role_input")
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        sql = "INSERT INTO ty_user(name, password,power,createtime,updatetime) VALUES ('" + str(
            name) + "' , '" + str(password) + "' , '" + str(power) + "' , '" + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "' , '" + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "' )"
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    return redirect('/user')


@csrf_exempt
def userlist():
    result = []
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        sql = "SELECT name,power,createtime,updatetime from ty_user"
        cursor.execute(sql)
        for item in cursor.fetchall():
            if item[1] == 1:
                power = "管理员"
            elif item[1] == 2:
                power = "开发人员"
            else:
                power = "游客"
            result.append(User(name=item[0], power=power, createtime=item[2].strftime("%Y-%m-%d %H:%M:%S"),
                               updatetime=item[3].strftime("%Y-%m-%d %H:%M:%S"), password=None))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    return result


class User:
    def __init__(self, name, power, createtime, updatetime, password):
        self.name = name
        self.password = password
        self.power = power
        self.createtime = createtime
        self.updatetime = updatetime


@csrf_exempt
def userupdate(request):
    if request.method == "POST":
        name = request.POST.get("mode_updateUser_name_input")
        olduser = selectbyname(name, "")[0]
        password = request.POST.get("mode_updateUser_password") if request.POST.get(
            "mode_updateUser_password") != "" else olduser.password
        power = request.POST.get("mode_updateUser_role_input") if request.POST.get(
            "mode_updateUser_role_input") != "" else olduser.power
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        sql = "UPDATE ty_user SET name = '" + str(name) + "',password = '" + str(password) + "',power = '" + str(
            power) + "',updatetime = '" + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "' WHERE name = '" + str(name) + "'"
        print(sql)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    return redirect('/user')


@csrf_exempt
def userdelete(request):
    if request.method == "POST":
        name = request.POST.get("mode_deleteUser_name")
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        sql = "DELETE from ty_user WHERE name = '" + str(name) + "'"
        print(sql)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    return redirect('/user')


def selectbyname(name, password):
    result = []
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        sql = "SELECT name,power,createtime,updatetime,password from ty_user WHERE name = '" + str(name) + "'"
        sql += "AND password = '" + str(password) + "'" if password != "" else ""
        cursor.execute(sql)
        for item in cursor.fetchall():
            if item[1] == 1:
                power = "管理员"
            elif item[1] == 2:
                power = "开发人员"
            else:
                power = "游客"
            result.append(User(name=item[0], power=power, createtime=item[2].strftime("%Y-%m-%d %H:%M:%S"),
                               updatetime=item[3].strftime("%Y-%m-%d %H:%M:%S"), password=item[4]))
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    return result


@csrf_exempt
def login(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password") if request.POST.get(
            "password") != "" else "%##!!!@##$$&**((^%#$@#!@@#$@##@#!!!$E$(_+2"
        person = selectbyname(name, password)
        if person is not None and len(person) > 0 and person[0].power == "管理员":
            # 管理者
            result = 1
            username = person[0].name
        elif person is not None and len(person) > 0 and person[0].power == "开发人员":
            # 开发者
            result = 2
            username = person[0].name
        else:
            # 游客
            result = 3
            username = "游客"
        return HttpResponse(json.dumps({
            "username": username,
            "result": result
        }))
