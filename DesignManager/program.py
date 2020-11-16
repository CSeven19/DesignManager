import os
import pymysql
from django.shortcuts import render, redirect
import time, datetime

from tyOTUI.update import Config


def init(request):
    context = {}
    context['ty_program_name'] =request.GET.get('name')
    context['programsubversions_ui'] = getAllProgramsOnVersionUI(context['ty_program_name'])
    context['programsubversions_ot'] = getAllProgramsOnVersionOT(context['ty_program_name'])
    context['ty_program_profile'] = getDescrible(context['ty_program_name'])
    context['ty_program_tag_list'] = getTags(context['ty_program_name'])
    context['mode_updateFile_lastSubVersionOnUI'] = getLastSubVersionOnUI(context['ty_program_name'])
    context['mode_updateFile_lastSubVersionOnOT'] = getLastSubVersionOnOT(context['ty_program_name'])
    context['ty_program_version_all'] = getAllProgramVersions(context['ty_program_name'])
    return render(request, 'program.html', context)


def getDescrible(name):
    result = ""
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        for describle in cursor.fetchall():
            result = str(describle)[2:-3]
    except:
    db.close()
    return result


def newprogramversion(request):
    if request.method == "POST":
        programName = request.POST.get("mode_createVersio_programname_input")
        programVersion = request.POST.get("mode_createVersion_version")
        if programVersion not in getAllProgramVersions(programName):
            saveprogramversion(programName, programVersion)


def saveprogramversion(programName, programVersion):
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def getAllProgramVersions(name):
    result = []
    db = pymysql.connect(**Config)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        for version in cursor.fetchall():
            result.append(str(version)[2:-3])
        result = list(set(result))
    except:
    db.close()
    return result


def getLastSubVersionOnUI(name):
    result = []
    programversions = getAllProgramVersions(name)
    programsubversions = getAllProgramsOnVersionUI(name)
    if programversions is not None:
        for programversion in programversions:  # [v3.1.1]
            maxsubversion = ""
            if programsubversions is not None:  # [v3.1.1.1,v3.2.1.1]
                for subversion in programsubversions:
                    # 同版本判断
                    if programversion == subversion[:subversion.rindex(".")]:
                        if maxsubversion == "":
                            maxsubversion = programversion + "." + str(int(subversion[subversion.rindex(".") + 1:]) + 1)
                        else:
                            if int(maxsubversion[maxsubversion.rindex(".") + 1:]) <= int(
                                    subversion[subversion.rindex(".") + 1:]):
                                maxsubversion = subversion[:subversion.rindex(".")] + "." + str(
                                    int(subversion[subversion.rindex(".") + 1:]) + 1)
            if maxsubversion == "":
                result.append(programversion + programversion + ".1")
            else:
                result.append(programversion + maxsubversion)
    return result


def getLastSubVersionOnOT(name):
    result = []
    programversions = getAllProgramVersions(name)
    programsubversions = getAllProgramsOnVersionOT(name)
    if programversions is not None:
        for programversion in programversions:
            maxsubversion = ""
            if programsubversions is not None:
                for subversion in programsubversions:
                    # 同版本判断
                    if programversion == subversion[:subversion.rindex(".")]:
                        if maxsubversion == "":
                            maxsubversion = programversion + "." + str(int(subversion[subversion.rindex(".") + 1:]) + 1)
                        else:
                            if int(maxsubversion[maxsubversion.rindex(".") + 1:]) <= int(
                                    subversion[subversion.rindex(".") + 1:]):
                                maxsubversion = subversion[:subversion.rindex(".")] + "." + str(
                                    int(subversion[subversion.rindex(".") + 1:]) + 1)
            if maxsubversion == "":
                result.append(programversion + programversion + ".1")
            else:
                result.append(programversion + maxsubversion)
    return result


class MyVersion:
    def __init__(self, filename, version, subversion, createtime):
        self.filename = filename
        self.version = version
        self.subversion = subversion
        self.createtime = createtime


class MyTag:
    def __init__(self, ab, name, versions):
        self.ab = ab
        self.name = name
        self.versions = versions


def getAllProgramsOnVersionUI(name):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
    for root, dirs, files in os.walk(dir, topdown=True):
        return dirs


def getAllProgramsOnVersionUITime(name):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
    times = []
    for root, dirs, files in os.walk(dir, topdown=True):
        if dirs is not None:
            for mdir in dirs:
                times.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(dir + "/" + mdir))))
            return times


def getAllProgramsOnVersionUIFilename(name):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
    filenames = []
    for root, dirs, files in os.walk(dir, topdown=True):
        if dirs is not None:
            for mdir in dirs:
                tempfilename = ""
                for mfile in os.listdir(os.path.join(dir, mdir)):
                    tempfiles = mfile.rsplit(".")
                    if (len(tempfiles) > 1):
                        if mfile.rsplit(".")[1] == "yaml":
                            filenames.append(mfile[:-5])
                            tempfilename = mfile[:-5]
                if tempfilename == "":
                    filenames.append("")
            return filenames


def getAllProgramsOnVersionOT(name):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
    for root, dirs, files in os.walk(dir, topdown=True):
        return dirs


def getAllProgramsOnVersionOTTime(name):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
    times = []
    for root, dirs, files in os.walk(dir, topdown=True):
        if dirs is not None:
            for mdir in dirs:
                times.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(dir + "/" + mdir))))
            return times


def getAllProgramsOnVersionOTFilename(name):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0][:-7]
    filenames = []
    for root, dirs, files in os.walk(dir, topdown=True):
        if dirs is not None:
            for mdir in dirs:
                tempfilename = ""
                for mfile in os.listdir(os.path.join(dir, mdir)):
                    tempfiles = mfile.rsplit(".")
                    if (len(tempfiles) > 1):
                        if mfile.rsplit(".")[1] == "yaml":
                            filenames.append(mfile[:-5])
                            tempfilename = mfile[:-5]
                if tempfilename == "":
                    filenames.append("")
            return filenames


def getTags(name):
    tags = []
    uis = []
    ots = []
    subversions_ui = getAllProgramsOnVersionUI(name)
    subversions_ot = getAllProgramsOnVersionOT(name)
    subversionstime_ui = getAllProgramsOnVersionUITime(name)
    subversionstime_ot = getAllProgramsOnVersionOTTime(name)
    subversionsfilenames_ui = getAllProgramsOnVersionUIFilename(name)
    subversionsfilenames_ot = getAllProgramsOnVersionOTFilename(name)
    if subversions_ui is not None:
        count = 0
        for subversion_ui in subversions_ui:
            uis.append(
                MyVersion(subversionsfilenames_ui[count], subversion_ui[:subversion_ui.rindex(".")], subversion_ui,
                          subversionstime_ui[count]))
            count += 1
    if subversions_ot is not None:
        count = 0
        for subversion_ot in subversions_ot:
            ots.append(
                MyVersion(subversionsfilenames_ot[count], subversion_ot[:subversion_ot.rindex(".")], subversion_ot,
                          subversionstime_ot[count]))
            count += 1
    uis.reverse()
    ots.reverse()
    return tags


def deleteversion(request):
    if request.method == "POST":
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(path)
