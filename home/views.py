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


# @csrf_exempt
# def add_post(request):
#     comment=request.POST.get("comment").split(",")
#     tags=request.POST.get("tags").split(",")
#     user_details={"first_name":request.POST.get("first_name"),"last_name":request.POST.get("last_name")}
#     post=Posts(post_title=request.POST.get("post_title"),post_description=request.POST.get("post_description"),comment=comment,tags=tags,user_details=user_details)
#     post.save()
#     return HttpResponse("Inserted")

# @csrf_exempt
# def update_post(request,id):
#     post=Posts.objects.get(_id=ObjectId(id))
#     post.user_details['first_name']=request.POST.get('first_name')
#     post.save()
#     return HttpResponse("Post Updated")

# def delete_post(request,id):
#     post=Posts.objects.get(_id=ObjectId(id))
#     post.delete()
#     return HttpResponse("Post Deleted")

# def read_post(request,id):
#     post=Posts.objects.get(_id=ObjectId(id))
#     stringval="First Name : "+post.user_details['first_name']+" Last name : "+post.user_details['last_name']+" Post Title "+post.post_title+" Comment "+post.comment[0]
#     return HttpResponse(stringval)

# def read_post_all(request):
#     posts=Posts.objects.all()
#     stringval=""
#     for post in posts:
#         stringval += "First Name : " + post.user_details['first_name'] + " Last name : " + post.user_details[
#             'last_name'] + " Post Title " + post.post_title + " Comment " + post.comment[0]+"<br>"

#     return HttpResponse(stringval)