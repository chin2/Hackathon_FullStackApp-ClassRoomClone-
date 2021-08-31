
from django.contrib import admin
from django.urls import path
from student import views
urlpatterns = [
    path('<str:id>/',views.studentpage,name='dashboard'),
    path('assignment/<str:id>/',views.assignment,name='assignment'),  
    path('test/<str:id>/',views.test,name='test'),  
    path('calendar/<str:id>/',views.calendar,name='calendar'),

    path('joinclass/<str:id>/',views.joinclass,name="joinclass"),
    path('viewmoreclass/<str:id>/<str:val>',views.viewMoreClass,name="viewMoreClass"),


    path("assignsubmit/<str:id>/<str:val>/<str:code>/",views.assignmentsubmit,name="assignmentsubmit"),
    path("testsubmit/<str:id>/<str:val>/<str:code>",views.testsubmit,name="testsubmit")
]
