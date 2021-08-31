from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import hashlib
# Create your views here.
from home.models import *

# def check_validate(request):
#     try:
#         print(request.session["email"])
#     except :
#         return render(request,"auth/login.html")

def secruity(func):
    def inner(request, id):
        if id in request.session:
            return func(request, id)
        else:
            return redirect("/")
    return inner

@secruity
def studentpage(request,id):
    classlist=[]
    for i in ClassRoom.objects.filter(students_id=id):
        classlist.append(i.__dict__)
    data={
        "title":"Dashboard",
        "user":request.session[id],
        "classlist":classlist
    }
    return render(request,'student/dashboard.html',data)
@secruity
def test(request,id):
    classlist=[]
    testlist=[]
    anstestlist=[]
    for i in ClassRoom.objects.filter(students_id=id):
        classlist.append(i.classcode)
    for i in classlist:
        for j in Test.objects.filter(classcode=i):
            testlist.append(j.__dict__)
    for i in TestMarks.objects.filter(studentid=id):
        anstestlist.append(i.__dict__)
    data={
        "title":"Test",
        "user":request.session[id],
        "testlist":testlist,
        "anstestlist":anstestlist
    }
    return render(request,'student/test.html',data)
@secruity
def assignment(request,id):
    classlist=[]
    assignmentlist=[]
    ansassignmentlist=[]
    for i in ClassRoom.objects.filter(students_id=id):
        classlist.append(i.classcode)
    for i in classlist:
        for j in Assignment.objects.filter(classcode=i):
            assignmentlist.append(j.__dict__)
    for i in AssignmentMarks.objects.filter(studentid=id):
        ansassignmentlist.append(i.__dict__)
    data={
        "title":"Assignment",
        "user":request.session[id],
        "assignmentlist":assignmentlist,
        "ansassignmentlist":ansassignmentlist
    }
    return render(request,'student/assignment.html',data)
@secruity
def calendar(request,id):
    classlist=[]
    calendarlist=[]
    for i in ClassRoom.objects.filter(students_id=id):
        classlist.append(i.classcode)
    for i in classlist:
        for j in Calendar.objects.filter(classcode=i):
            calendarlist.append(j)
    data={
        "title":"Calendar",
        "user":request.session[id],
        "calendarlist":calendarlist
    }
    return render(request,'student/calendar.html',data)
@secruity
def joinclass(request,id):
    classcode=request.GET.get("classcode",None)
    signup=Signup.objects.get(pk=id)
    if ClassRoom.objects.filter(classcode=classcode).exists():
        classcode=ClassRoom.objects.get(classcode=classcode)
        classcode.students.add(signup)
        classcode.save()
        return redirect("dashboard",id=id)
    # return redirect("dashboard",id=id)
    data={
        "title":"Dashboard",
        "user":request.session[id],
        "classnotfound":"Invalid Class Code "
    }
    return render(request,"student/dashboard.html",data)

def assignmentsubmit(request,id,val,code):
    # print(id,pk)
    studentid=id
    classcode=code
    assignmentid=val
    assignmentStatus="Submitted"
    inputfile=request.FILES["ifile"]
    fs=FileSystemStorage()
    fileapploaded=fs.url(fs.save(inputfile.name,inputfile))
    a=AssignmentMarks.objects.create(studentid=studentid,assignmentStatus=assignmentStatus,classcode=classcode,fileapploaded=fileapploaded)
    assignment=Assignment.objects.get(pk=assignmentid)
    assignment.studentMarkList.add(a)
    assignment.save()
    return redirect("assignment",id=id)

def testsubmit(request,id,val,code):
    # print(id,pk)
    studentid=id
    assignmentid=val
    classcode=code
    teststatus="Submitted"
    inputfile=request.FILES["ifile"]
    fs=FileSystemStorage()
    fileapploaded=fs.url(fs.save(inputfile.name,inputfile))
    a=TestMarks.objects.create(studentid=studentid,teststatus=teststatus,fileapploaded=fileapploaded,classcode=classcode)
    test=Test.objects.get(pk=assignmentid)
    test.studentMarkList.add(a)
    test.save()
    return redirect("test",id=id)

def viewMoreClass(request,id,val):
    a=ClassRoom.objects.get(classcode=val).__dict__
    data={
        "title":"Dashboard"+" "+val,
        "user":request.session[id],
        "classdetails":a
    }
    return render(request,"student/viewmore.html",data)

