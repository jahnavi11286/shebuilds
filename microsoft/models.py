from django.db import models

# Create your models here.
class adminuser(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=30)
    organisationcode=models.CharField(max_length=30)
    class Meta:
        unique_together=["email","organisationcode"]

class examdetails(models.Model):
    email=models.CharField(max_length=50)
    examid=models.CharField(max_length=50)
    exampassword=models.CharField(max_length=50)
    examname=models.CharField(max_length=50)
    noq=models.CharField(max_length=3)
    class Meta:
        unique_together=["email","examid"]

class questions(models.Model):
    examid=models.CharField(max_length=50)
    questionno=models.CharField(max_length=3)
    question=models.CharField(max_length=250)
    option1=models.CharField(max_length=50)
    option2=models.CharField(max_length=50)
    option3=models.CharField(max_length=50)
    option4=models.CharField(max_length=50)
    solution=models.CharField(max_length=3)

class studentface(models.Model):
    email=models.CharField(max_length=50)
    studentid=models.CharField(max_length=30,null=False,blank=False,unique=True)
    url=models.CharField(max_length=100,null=False,blank=False)

class attendence(models.Model):
    studentid=models.CharField(max_length=30,null=False,blank=False)
    date=models.CharField(max_length=30,null=False,blank=False)
    time=models.CharField(max_length=30,null=False,blank=False)
    status=models.CharField(max_length=30,null=False,blank=False)

class examattend(models.Model):
    studentid=models.CharField(max_length=30,null=False,blank=False)
    examid=models.CharField(max_length=50)
    date=models.CharField(max_length=30,null=False,blank=False)
    time=models.CharField(max_length=30,null=False,blank=False)
    score=models.CharField(max_length=30,null=False,blank=False)