from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('newexam/',views.newexam,name='newexam'),
    path('newquestion/',views.newquestion,name='newquestion'),
    path('addstudent/',views.addstudent,name='addstudent'),
    path('takeexam/',views.takeexam,name="takeexam"),
    path('verifyface/',views.verifyface,name="verifyface"),
    path('myexams/',views.myexams,name="myexams"),
    path('download/',views.download,name="download")
]