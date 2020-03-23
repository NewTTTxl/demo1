from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from .models import *
from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request, 'html/index.html')
def teacher(request):
    return render(request,'html/teacher.html')
def student(request):
    return render(request,'html/student.html')
def shenpi(request):
    return render(request,'html/shenpi.html')
def shenpiok(request):
    return render(request,'html/shenpiok.html')

def teacher_list(request):
    teachers=Teacher.objects.all()
    list_teacher=[]
    for i in teachers:
        collections = {}
        collections['name']=i.name
        collections['content']=i.content
        collections['gender']=i.gender
        collections['major'] = i.major
        list_teacher.append(collections)
    return JsonResponse({'data':list_teacher})

def student_list(request):
    students=Student.objects.all()
    list_student=[]
    for i in students:
        collections = {}
        collections['name']=i.name
        collections['content']=i.content
        collections['gender']=i.gender
        list_student.append(collections)
    return JsonResponse({'data':list_student})
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        content = request.POST.get('content')
        gender = request.POST.get('gender',0)
        major = request.POST.get('major')
        types = request.POST.get('types')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if int(types)==0:
            teacher = Teacher(name=name,content=content,gender=gender,major=major,types=int(types),username=username,password=password)
            teacher.save()
        else:
            student = Student(name=name, content=content, gender=gender,types=int(types), username=username,password=password)
            student.save()
        return JsonResponse({'data':'注册成功！'})
    else:
        return render(request, 'register.html')
def login(request):
    if request.method == "POST":
        print(request.body)
        types = request.POST.get('types')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if int(types)==0:
            teacher=Teacher.objects.filter(username=username,password=password).first()
            if teacher:
                request.session['user_id'] = teacher.id
                request.session['types'] = types
                return JsonResponse({'data':'login success'})
            else:
                return redirect("/login/")
        else:
            student = Student.objects.filter(username=username, password=password).first()
            if student:
                request.session['user_id'] = student.id
                request.session['types'] = types
                return JsonResponse({'data':'login success'})
            else:
                return redirect("/login/")
    else:
        return render(request,'login2.html')

def logout(request):
    request.session.flush()
    return HttpResponse('logout success')

def choose_ts(request):
    if request.method=="POST":
        user_id=request.session.get('user_id')
        start_role=request.session.get('types')
        # user_id =1
        # start_role = 1
        name =  request.POST.get('name')
        # chhose_type = request.POST.get('chhoose_type')
        if int(start_role)==0:
            student_id=Student.objects.get(name=name)
            teacher_id=Teacher.objects.get(id=user_id)
            ts=TeacherandStudent.objects.create(teacher_id=teacher_id,student_id=student_id,teacher_flag=1,student_flag=0,start_role=start_role)
            ts.save()
            return JsonResponse({'data': '选择学员成功！'})
        else:
            teacher_id = Teacher.objects.get(name=name)
            student_id = Student.objects.get(id=user_id)
            ts = TeacherandStudent.objects.create(teacher_id=teacher_id, student_id=student_id, teacher_flag=0,
                                                  student_flag=1, start_role=start_role)
            ts.save()
            return JsonResponse({'data': '选择教师成功！'})
#审核
def check_status(request):
    user_id = request.session.get('user_id')
    login_start_role = request.session.get('types')
    if request.method=='GET':
        if int(login_start_role) == 0:
            teacher_id = Teacher.objects.get(id=user_id)
            ts = TeacherandStudent.objects.filter(teacher_id=teacher_id,start_role=1,teacher_flag=0)
            list_all=[]
            for i in ts:
                collections={}
                collections['name']=i.student_id.name
                collections['student_id'] = i.student_id.id
                collections['createTime'] = (i.createTime).strftime("%Y-%m-%d %H:%M:%S")
                list_all.append(collections)
            return JsonResponse({'data': list_all,'msg':'我的待审核学员！'})
        else:
            student_id = Student.objects.get(id=user_id)
            ts = TeacherandStudent.objects.filter(student_id=student_id, start_role=0, student_flag=0)
            list_all = []
            for i in ts:
                collections = {}
                collections['name'] = i.teacher_id.name
                collections['student_id'] = i.teacher_id.id
                collections['createTime'] = (i.createTime).strftime("%Y-%m-%d %H:%M:%S")
                list_all.append(collections)
            return JsonResponse({'data': list_all, 'msg': '我的待审核教师！'})
    else:
        name = request.POST.get('name')
        if int(login_start_role) == 0:
            student_id = Student.objects.get(name=name)
            TeacherandStudent.objects.filter(student_id=student_id,start_role=1).update(teacher_flag=1)
            return JsonResponse({'data': '教员审核学员成功！！！'})
        else:
            teacher_id = Teacher.objects.get(name=name)
            TeacherandStudent.objects.filter(teacher_id=teacher_id, start_role=0).update(student_flag=1)
            return JsonResponse({'data': '学员审核教员成功！！！'})

def show_all(request):
    user_id = request.session.get('user_id')
    start_role = request.session.get('types')
    if request.method=='GET':
        if int(start_role) == 0:
            teacher_id = Teacher.objects.get(id=user_id)
            ts = TeacherandStudent.objects.filter(teacher_id=teacher_id,start_role=1,teacher_flag=1)
            list_all=[]
            for i in ts:
                collections={}
                collections['name']=i.student_id.name
                collections['student_id'] = i.student_id.id
                collections['createTime'] = (i.createTime).strftime("%Y-%m-%d %H:%M:%S")
                list_all.append(collections)
            return JsonResponse({'data': list_all,'msg':'我的已经待审核学员！'})
        else:
            student_id = Student.objects.get(id=user_id)
            ts = TeacherandStudent.objects.filter(student_id=student_id, start_role=0, student_flag=1)
            list_all = []
            for i in ts:
                collections = {}
                collections['name'] = i.teacher_id.name
                collections['student_id'] = i.teacher_id.id
                collections['createTime'] = (i.createTime).strftime("%Y-%m-%d %H:%M:%S")
                list_all.append(collections)
            return JsonResponse({'data': list_all, 'msg': '我的已经审核教师！'})
