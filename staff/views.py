from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import hashlib,random,string
# Create your views here.
from datetime import datetime
from home.models import *
from django.core.files.storage import FileSystemStorage


def createClassCode():
    big=string.ascii_uppercase
    num="".join([str(i) for i in range(0,10)])
    code=big+num
    length=5
    return "".join(random.sample(code,length))

def secruity(func):
    def inner(request, id):
        if id in request.session:
            return func(request, id)
        else:
            return redirect("/login/")
    return inner

@secruity
def classList(request,id):
    classlist=[]
    for i in ClassRoom.objects.filter(teacher=id):
        classlist.append(i.__dict__)
    data={
        "title":"Class List",
        "user":request.session[id],
        "newCode":createClassCode(),
        "classlist":classlist
    }
    return render(request,'staff/classlist.html',data)

@secruity
def testlist(request,id):
    classlist=[]
    testlist=[]
    cl=[]
    anstestlist=[]
    for i in ClassRoom.objects.filter(teacher=id):
        classlist.append(i.__dict__)
        cl.append(i.classcode)
    for i in cl:
        for j in TestMarks.objects.filter(classcode=i):
            anstestlist.append(j.__dict__)  
    for i in Test.objects.filter(teacher=id)[::-1]:
        testlist.append(i.__dict__)
    data={
        "title":"Test List",
        "user":request.session[id],
        "classlist":classlist,
        "testlist":testlist,
        "anstestlist":anstestlist
    }
    return render(request,'staff/testlist.html',data)
    
@secruity
def assignmentlist(request,id):
    classlist=[]
    assignmentlist=[]
    cl=[]
    ansassignmentlist=[]
    for i in ClassRoom.objects.filter(teacher=id):
        classlist.append(i.__dict__)
        cl.append(i.classcode)
    for i in cl:
        for j in AssignmentMarks.objects.filter(classcode=i):
            ansassignmentlist.append(j.__dict__)

    for i in Assignment.objects.filter(teacher=id)[::-1]:

        assignmentlist.append(i.__dict__)
    data={
        "title":"Assignment List",
        "user":request.session[id],
        "classlist":classlist,
        "assigmentlist":assignmentlist,
        "ansassignmentlist":ansassignmentlist
    }
    return render(request,'staff/assignmentlist.html',data)


@secruity
def calendarlist(request,id):
    cl=[]
    calendarlist=[]
    for i in ClassRoom.objects.filter(teacher=id):
        cl.append(i.classcode)
    for i in Calendar.objects.filter(teacherid=id):
        calendarlist.append(i.__dict__)
    
    data={
        "title":"Calendar",
        "user":request.session[id],
        "classlist":cl,
        "calendarlist":calendarlist
    }
    return render(request,'staff/calendar.html',data)

@secruity
def createclass(request,id):
    data={
        "success":False,
        "err":"",
        "data":[],
        "description":""
    }
    classcode=request.POST.get("classcode",None)
    classname=request.POST.get("classname",None)
    description=request.POST.get("description",None)
    if ClassRoom.objects.filter(classcode=classcode).exists():
        data['description']="dublicated class code"
        return JsonResponse(data)
    else:
        a=Signup.objects.get(id=id)
        ClassRoom.objects.create(classcode=classcode,classname=classname,classdescription=description,teacher=a)
        data["success"]=True
        data["description"]='created successfully'
    return JsonResponse(data)        

    # return 

def assignmentcreate(request,id):
    if request.method=="POST":
        inputfile=request.FILES["inputfile"]
        fs=FileSystemStorage()
        name=fs.url(fs.save(inputfile.name,inputfile))
        classcode=request.POST.get("classcode",None)
        # duetime=datetime.fromisoformat(request.POST.get("duetime",None)[:-1])
        # duetime=duetime.strftime("%Y-%m-%d %H:%M:%S")
        duetime=request.POST.get("duetime",None)
        heading=request.POST.get("heading",None)
        marks=request.POST.get("marks",None)
        description=request.POST.get("description",None)
        

        classcode=request.POST.get("classcode",None)
        signup=id
        classroom=ClassRoom.objects.get(pk=classcode)
        # return HttpResponse(duetime)
        Assignment.objects.create(teacher=signup,classcode=classroom,heading=heading,\
            description=description,file=name,marks=marks,\
            date=duetime)
    return redirect("assignmentlist",id=id)

def testcreate(request,id):
    if request.method=="POST":
        inputfile=request.FILES["inputfile"]
        classcode=request.POST.get("classcode",None)
        duetime=request.POST.get("duetime",None)
        heading=request.POST.get("heading",None)
        marks=request.POST.get("marks",None)
        description=request.POST.get("description",None)
        fs=FileSystemStorage()
        name=fs.url(fs.save(inputfile.name,inputfile))
        classcode=request.POST.get("classcode",None)
        signup=str(id)
        # return HttpResponse(duetime)
        Test.objects.create(teacher=signup,classcode=classcode,heading=heading,description=description,file=name,marks=marks,date=duetime)
    return redirect("testlist",id=id)


def createmeeting(request,id):
    if request.method=="POST":
        classcode=request.POST.get("classcode",None)
        classtime=request.POST.get("classtime",None)
        link=request.POST.get("link",None)
        Calendar.objects.create(classcode=classcode,date=classtime,link=link,teacherid=id )
    return redirect("calendarlist",id=id)

def updateAssignmentMark(request,id,val):
    mark=request.GET.get("marks",None)
    a=AssignmentMarks.objects.get(id=val)
    a.studentMarks=mark
    a.assignmentStatus="markgiven"
    a.save()
    return redirect("assignmentlist",id=id)

def updateTestMark(request,id,val):
    mark=request.GET.get("marks",None)
    a=TestMarks.objects.get(id=val)
    a.studentMarks=mark
    a.teststatus="markgiven"
    a.save()

    return redirect("testlist",id=id)

def viewMoreDetail(request,id,val):
    a=ClassRoom.objects.get(classcode=val).__dict__
    data={
        "title":"Dashboard"+" "+val,
        "user":request.session[id],
        "classdetails":a
    }
    return render(request,"staff/viewmoredetail.html",data)
