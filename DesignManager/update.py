import os
import zipfile

import shutil

import pymysql
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

Config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "tyotui"
}


def updatefile(request):
    if request.method == "POST":
        programName = request.POST.get("mode_updateFile_programName_input")
        programVersion = request.POST.get("mode_updateFile_programVersion_input")
        programUpdateType = request.POST.get("mode_updateFile_updateType_input")
        programLastSubVersion = request.POST.get("mode_updateFile_lastSubVersion_input")
        srcFile = request.FILES.get("srcFile")
        # 文件根路径获取注意截取掉项目名一次
        root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
        desDir = root_path + "/static/" + request.POST.get("mode_updateFile_des_input").replace("\\", "/")
        # desFile = os.path.join(desDir, srcFile.name).replace("\\", "/")
        tempDir = root_path + "/static/temp"
        deleteTemp(tempDir, programName)
        tempFile = os.path.join(tempDir, srcFile.name).replace("\\", "/")
        if not os.path.exists(tempDir):
            # 新建文件夹
            os.makedirs(tempDir)
            with open(tempFile, mode="wb+") as des:
                for chunck in srcFile.chunks():
                    des.write(chunck)
        else:
            with open(tempFile, mode="wb+") as des:
                for chunck in srcFile.chunks():
                    des.write(chunck)
        # 解压缩包
        #     tempFile = r"D:\Users\Administrator\PycharmProjects\tyOTUI\static\temp\原型-版本管理.zip"
        #     tempDir = r"D:\Users\Administrator\PycharmProjects\tyOTUI\static\temp"
        #     desDir = r"D:\Users\Administrator\PycharmProjects\tyOTUI\static\UI\cpip4-云搜\3.0.22"
        extracFile(tempFile, tempDir, desDir)
        deleteTemp(tempDir, programName)
        # 新建个包含封装文件夹名的yaml文件用于之后生成版本展示中的文件名
        paths = os.path.split(tempFile)
        desFile = os.path.join(desDir, paths[1][:-4] + ".yaml")
        with open(desFile, mode="w"):
            pass


def deleteTemp(tempDir, programName):
    # 删除临时文件
    for root, dirs, files in os.walk(tempDir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def extracFile(source_dir, temp_dir, target_ir):
    with zipfile.ZipFile(source_dir, 'r', zipfile.ZIP_DEFLATED) as zf:
        for file in zf.namelist():
            try:
                filename = file.encode('cp437').decode('gbk')  # 先使用cp437编码，然后再使用gbk解码
            except:
                filename = file.encode('utf-8').decode('utf-8')
            zf.extract(file, temp_dir)  # 解压缩ZIP文件
            os.chdir(temp_dir)  # 切换到目标目录
            os.rename(file, filename)  # 重命名文件
    if os.path.exists(source_dir[:-4]):
        src = source_dir[:-4]
    else:
        src = temp_dir
        if os.path.exists(source_dir):
            os.remove(source_dir)
    shutil.copytree(src, target_ir)