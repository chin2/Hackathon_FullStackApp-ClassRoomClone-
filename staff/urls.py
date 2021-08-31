
from django.contrib import admin
from django.urls import path
from staff import views


urlpatterns = [
    path('<str:id>/',views.classList,name='classlist'),  
    path('testlist/<str:id>/',views.testlist,name='testlist'),  
    path('assignmentlist/<str:id>/',views.assignmentlist,name='assignmentlist'),
    path('calendarlist/<str:id>/',views.calendarlist,name='calendarlist'),


    path('<str:id>/class/create/',views.createclass,name="createclasslist"),
    path('assignmentcreate/<str:id>',views.assignmentcreate,name="assignmentcreate"),
    path('createmeeting/<str:id>',views.createmeeting,name="createmeeting"),
    path('testcreate/<str:id>',views.testcreate,name="testcreate"),

    path('updateassignmentmark/<str:id>/<str:val>/',views.updateAssignmentMark,name="updateAssignmentMark"),
    path('updatetestmark/<str:id>/<str:val>/',views.updateTestMark,name="updateTestMark"),

    path('viewmoredetail/<str:id>/<str:val>',views.viewMoreDetail,name="viewMoreDetail"),


]
