from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import adminuser,examdetails,questions,studentface,attendence,examattend
import requests
import csv
import datetime
import io
from io import BytesIO
from azure.storage.blob import  BlobServiceClient,ContentSettings
import json
import base64,urllib
from django.core.files.base import ContentFile
import numpy as np
import urllib.parse as urlparse
import os
from collections import Counter

# Create your views here.
que=0
score=0
presol="n"

def home(request):
    clients=adminuser.objects.all().count()
    exams=examdetails.objects.all().count()
    students=studentface.objects.all().count()
    context={
    'clients':clients,
    'exams':exams,
    'students':students
    }
    return render(request,'home.html',context)

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            User=adminuser.objects.get(email=request.POST.get('email'))
        except:
            return redirect('signup')
        if password==User.password:
            request.session['email']=email
            return redirect('adminhome')
    return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        organisation=request.POST.get('organization')
        if password==confirmpassword:
            User=adminuser()
            User.email=email
            User.password=password
            User.organisationcode=organisation
            try:
                User.save()
            except:
                return redirect('login')
            request.session['email']=email
            return redirect('adminhome')

    return render(request,'signup.html')

def logout(request):
    del request.session['email']
    return redirect('home')

def adminhome(request):
    if 'email' in request.session:
        clients=adminuser.objects.filter(email=request.session['email']).count()
        exams=examdetails.objects.filter(email=request.session['email']).count()
        students=studentface.objects.filter(email=request.session['email']).count()
        context={
        'clients':clients,
        'exams':exams,
        'students':students
        }
        return render(request,'adminhome.html',context)
    return redirect('login')

def newexam(request):
    if 'email' in request.session:
        if request.method=="POST":
            Exam=examdetails()
            if request.POST.get('exampassword')==request.POST.get('confirmpassword'):
                Exam.email=request.session['email']
                Exam.examid=request.POST.get('examid')
                Exam.examname=request.POST.get('examname')
                Exam.exampassword=request.POST.get('exampassword')
                Exam.noq=request.POST.get('noq')
                Exam.save()
                return redirect('newquestion')
        return render(request,'newexam.html')
    return redirect('login')

def newquestion(request):
    if 'email' in request.session:
        if request.method=="POST":
            examid=request.POST.get('examid')
            Exam=examdetails.objects.get(examid=examid)
            if Exam.email==request.session['email']:
                totalnoq=questions.objects.filter(examid=examid).count()
                if totalnoq<int(request.POST.get('qno')):
                    Question=questions()
                    Question.examid=examid 
                    Question.question=request.POST.get('question')
                    Question.questionno=request.POST.get('qno')
                    Question.option1=request.POST.get('option1')
                    Question.option2=request.POST.get('option2')
                    Question.option3=request.POST.get('option3')
                    Question.option4=request.POST.get('option4')
                    Question.solution=request.POST.get('crtopt')
                    Question.save()
                    return render(request,"newquestion.html")
                else:
                    return redirect('adminhome')
        return render(request,"newquestion.html")
    return redirect('login')

def addstudent(request):
    if 'email' in request.session:
        context={
        "attendence":True
        }
        if request.method=="POST":
            studentid=request.POST.get('studentid')
            if request.POST.get("action")=="upload":
                img_data=request.POST.get('photodata')
                format, imgstr = img_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr))
                file_name=studentid
                connect_str="DefaultEndpointsProtocol=https;AccountName=myazurecontainer1;AccountKey=XRe8+z8f4V7U9mKNU72o9sd4l3TN3+qcN1D6ctgUP8eeFA/Db9+Ugml5U9sFS88P8xC2vJ71vIAC+ASt6LzF3g==;EndpointSuffix=core.windows.net"
                blob_service_client = BlobServiceClient.from_connection_string(connect_str)
                container_name="myazurecontainer"
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name+'.png')
                try:
                    blob_client.upload_blob(data)
                except:
                    return HttpResponse("<h1>Student details are added already</h1>")
                print(blob_client.url)
                Studentface=studentface()
                Studentface.studentid=studentid
                Studentface.url=blob_client.url
                Studentface.email=request.session['email']
                Studentface.save()
                return redirect('addstudent')
            if request.POST.get("action")=="take":
                img_data=request.POST.get('photodata')
                format, imgstr = img_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr))
                sub_key='249505c284fb46f5828d4caf793bb041'
                try:
                    Studentface=studentface.objects.get(studentid=studentid)
                except:
                    return HttpResponse("Student id not found!")
                file1=Studentface.url
                print(file1)
                response=requests.get(file1)
                img_data1=BytesIO(response.content)
                uri_base="https://jahnavi.cognitiveservices.azure.com/"
                headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': sub_key,
                }
                headers2={
                    'Content-Type': 'application/json',
                    'Ocp-Apim-Subscription-Key': sub_key,
                }
                params = {
                    'returnFaceId': 'true',
                }
                img_list=[]
                face_api1='/face/v1.0/detect'
                face_api2='/face/v1.0/verify'
                img_list.append(data)
                img_list.append(img_data1)
                faceid_list=[]
                try:
                    for img in img_list:
                        response=requests.post(uri_base+face_api1,
                            data=img,
                            headers=headers,
                            params=params
                            )
                        parsed=response.json()
                        print(parsed)
                        json_str=parsed[0]
                        faceid_list.append(json_str['faceId'])
                except Exception as e:
                    return HttpResponse("<h1>"+e+"</h1>")
                print(faceid_list)
                data={"faceId1":faceid_list[0],"faceId2":faceid_list[1]}
                data_json=json.dumps(data)
                response=requests.post(uri_base + face_api2,data=data_json,headers=headers2)
                parsed=response.json()
                if parsed['isIdentical']:
                    Attendence=attendence()
                    Attendence.studentid=studentid
                    x = datetime.datetime.now()
                    str1 = x.strftime('%m/%d/%y-%H:%M:%S')
                    y=str1.split("-")
                    Attendence.date=y[0]
                    Attendence.time=y[1]
                    Attendence.status="present"
                    Attendence.save()
                    return redirect("addstudent")
                else:
                    return HttpResponse("Student Face not identical!")
        return render(request,"addstudent.html",context)
    return redirect('login')

def verifyface(request):
    context={
        "attendence":False
        }
    if request.method=="POST":
        img_data=request.POST.get('photodata')
        format, imgstr = img_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))
        sub_key='249505c284fb46f5828d4caf793bb041'
        Userface=studentface.objects.get(studentid=request.session['examuserid'])
        file1=Userface.url
        print(file1)
        response=requests.get(file1)
        img_data1=BytesIO(response.content)
        uri_base="https://jahnavi.cognitiveservices.azure.com/"
        headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': sub_key,
        }
        headers2={
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': sub_key,
        }
        params = {
            'returnFaceId': 'true',
        }
        img_list=[]
        face_api1='/face/v1.0/detect'
        face_api2='/face/v1.0/verify'
        img_list.append(data)
        img_list.append(img_data1)
        faceid_list=[]
        try:
            for img in img_list:
                response=requests.post(uri_base+face_api1,
                    data=img,
                    headers=headers,
                    params=params
                    )
                parsed=response.json()
                print(parsed)
                json_str=parsed[0]
                faceid_list.append(json_str['faceId'])
        except Exception as e:
            return HttpResponse("<h1>"+e+"</h1>")
        print(faceid_list)
        data={"faceId1":faceid_list[0],"faceId2":faceid_list[1]}
        data_json=json.dumps(data)
        response=requests.post(uri_base + face_api2,data=data_json,headers=headers2)
        parsed=response.json()
        if parsed['isIdentical']:
            request.session['faceconfirm']=True
            request.session['first']=True
            return redirect('takeexam')
        else:
            return HttpResponse('<h1>Face id doesnt match please try again.</h1>')
    return render(request,"addstudent.html",context)

def takeexam(request):
    global que
    global score
    global presol
    context={
    "show":"a"
    }
    if 'first' in request.session and 'faceconfirm' in request.session:
            if not request.session['faceconfirm']:
                return redirect('verifyface')
            if request.session['first']:
                request.session['first']=False
                que=request.session['noq']
                question=questions.objects.get(examid=request.session['examid'],questionno="1")
                presol=question.solution
                context={
                "show":"que",
                "question":question.question,
                "qno":question.questionno,
                "nextqno":int(question.questionno)+1,
                "option1":question.option1,
                "option2":question.option2,
                "option3":question.option3,
                "option4":question.option4
                }
                return render(request,'takeexam.html',context)

    if request.method=="POST":
        if request.POST.get('submit')=="take":
            examid=request.POST.get('examid')
            Exam=examdetails.objects.get(examid=examid)
            if Exam.exampassword==request.POST.get('exampassword'):
                request.session['examid']=Exam.examid
                request.session['examuserid']=request.POST.get('stuid')
                request.session['noq']=Exam.noq
                score=0
                return redirect('verifyface')
            else:
                return HttpResponse("<h1>Wrong details!</h1>")

        if request.POST.get('submit')=="Next" and request.session['faceconfirm']:
            if "examuserid" in request.session:
                qno=request.POST.get("qno")
                print(que)
                if int(qno)>int(que):
                    que=0
                    if request.POST.get('options')==presol:
                        score=score+1
                    Attendence=examattend()
                    Attendence.studentid=request.session['examuserid']
                    Attendence.examid=request.session['examid']
                    x = datetime.datetime.now()
                    str1 = x.strftime('%m/%d/%y-%H:%M:%S')
                    y=str1.split("-")
                    Attendence.date=y[0]
                    Attendence.time=y[1]
                    Attendence.score=score
                    Attendence.save()
                    del request.session['examid']
                    del request.session['examuserid']
                    del request.session['faceconfirm']
                    del request.session['noq']
                    context={
                    "show":"end",
                    "score":score
                    }
                else:
                    question=questions.objects.get(examid=request.session['examid'],questionno=qno)
                    if request.POST.get('options')==presol:
                        score=score+1
                    presol=question.solution
                    context={
                    "show":"que",
                    "question":question.question,
                    "qno":question.questionno,
                    "nextqno":int(question.questionno)+1,
                    "option1":question.option1,
                    "option2":question.option2,
                    "option3":question.option3,
                    "option4":question.option4
                    }
            return render(request,'takeexam.html',context)
    return render(request,'takeexam.html',context)

def myexams(request):
    if not 'email' in request.session:
        return redirect('login')
    data=examdetails.objects.filter(email=request.session['email'])
    context={
    "view":"a",
    "exam_d":data
    }
    if request.method=="POST":
        data=examattend.objects.filter(examid=request.POST.get('examid'))
        context={
        "view":"b",
        "exam_d":data
        }
    return render(request,"myexams.html",context)

def download_csv(request, queryset):
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

def download(request):
    if 'email' in request.session:
        data=download_csv(request,examattend.objects.all())
        return HttpResponse(data,content_type='text/csv')
    else:
        return redirect('login')