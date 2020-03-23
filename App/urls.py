from django.urls import path,re_path,include
from . import views
app_name='App'


urlpatterns=[
    path('index/',views.index,name='index'),
    path('teacher/',views.teacher,name='teacher'),
    path('student/', views.student, name='student'),
    path('teacher_list/',views.teacher_list,name='teacher_list'),
    path('student_list/',views.student_list,name='student_list'),
    path('choose_ts/', views.choose_ts, name='choose_ts'),
    path('check_status/', views.check_status, name='check_status'),
    path('shenpi/', views.shenpi, name='shenpi'),
    path('shenpiok/', views.shenpiok, name='shenpiok'),
    path('show_all/', views.show_all, name='show_all'),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),

]