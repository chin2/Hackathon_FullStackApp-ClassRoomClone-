from django.shortcuts import render,redirect
from django.http import HttpResponse
import hashlib
# Create your views here.
from .models import *

def login(request):
    if request.method=="GET":
        return render(request, "auth/login.html")
    else:
        data={
            "data":"",
            "status":False,
            "error":"",
            "description":""
        }
        email=request.POST["email"]
        password=hashlib.md5((request.POST["password"]).encode()).digest()
        if Signup.objects.filter(email=email,password=password).exists():
            data["status"]=True
            a=Signup.objects.get(email=email,password=password)
            request.session[str(a.id)]= {
                "id":str(a.id),
                "email":a.email,
                "username":a.username,
                "userrole":a.role,
                "userimage":a.userimage
            }
            # request.session["email"]=a.email
            # request.session["username"]=a.username
            # request.session["userimage"]=a.userimage
            # request.session["userid"]=str(a.id)
            # request.session["userrole"]=a.role
            # print(request.session["email"])
            if Signup.objects.get(email=email,password=password).role=="Teacher":
                return redirect("/staff/%s/"%a.id)
            else:
                return redirect("/student/%s/"%a.id)
      
    data["descripion"]="Username / password mismatch"
    return render(request,"auth/login.html",{"des":"Username / password mismatch"})

def signup(request):
    if (request.method == "GET"):
        return render(request,"auth/signup.html")
    else:
        data={
            "status":False,
            "data":[],
            "error":"",
            "description":""
        }
        username=request.POST["username"]
        email=request.POST["email"]
        password=hashlib.md5((request.POST["password"]).encode()).digest()
        role=request.POST["dasignation"]
        print(request.POST)
        if Signup.objects.filter(email=email).exists():
            return render(request,"auth/signup.html",{"des":"email already exists"})
        s=Signup(email=email,username=username,password=password,role=role)
        s.save()
        return redirect("/login/",des="Username / password mismatch")

