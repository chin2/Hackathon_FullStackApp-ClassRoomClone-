from datetime import datetime,timedelta,date 
import uuid
from djongo import models
import django
class Signup(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.CharField(max_length=255)
    username=models.CharField(max_length=100)
    userimage=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=200,default="")
    role=models.CharField(max_length=200,default="Student")
    def __str__(self):
        return str(self.id)
# ClassRoom.objects.create(classcode="ljfa2",classname="ds",classdescription="hello",signupid="612a09768d3e252d8dddcbb3")

class ClassRoom(models.Model):
    # id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher=models.CharField(max_length=100)
    students = models.ArrayReferenceField(
        to=Signup,
        related_name="signup"
    )
    classcode=models.CharField(max_length=10,primary_key=True)
    classname=models.CharField(max_length=100)
    classdescription=models.CharField(max_length=1000)
    def __str__(self):
        return self.classcode

class AssignmentMarks(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classcode=models.CharField(max_length=100)
    studentid=models.CharField(max_length=100)
    studentMarks=models.CharField(max_length=100)
    fileapploaded=models.CharField(max_length=100)
    assignmentStatus=models.CharField(max_length=100,default="submitted")
    date=models.DateField(default=django.utils.timezone.now)

class Assignment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher=models.CharField(max_length=100)
    classcode=models.CharField(max_length=100)
    heading=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    file=models.CharField(max_length=100)
    marks=models.CharField(max_length=100)
    date=models.DateTimeField(default=date.today()+timedelta(days=1))
    studentMarkList = models.ArrayReferenceField(
        to=AssignmentMarks,
        on_delete=models.CASCADE,
    )

class TestMarks(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studentid=models.CharField(max_length=100)
    classcode=models.CharField(max_length=100)
    studentMarks=models.CharField(max_length=100)
    fileapploaded=models.CharField(max_length=100)
    teststatus=models.CharField(max_length=100,default="submitted")
    date=models.DateField(default=django.utils.timezone.now)

class Test(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classcode=models.CharField(max_length=100)
    teacher=models.CharField(max_length=100)
    heading=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    file=models.CharField(max_length=100)
    marks=models.CharField(max_length=100)
    date=models.DateTimeField(default=date.today()+timedelta(days=1))
    studentMarkList = models.ArrayReferenceField(
        to=TestMarks,
        on_delete=models.CASCADE,
    )

class Calendar(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacherid=models.CharField(max_length=100)
    classcode=models.CharField(max_length=100)
    date=models.DateTimeField(default=django.utils.timezone.now)
    link=models.CharField(max_length=10000)






