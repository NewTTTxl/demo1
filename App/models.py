from django.db import models

# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    gender = models.CharField(max_length=5)
    major = models.CharField(max_length=20)
    types = models.IntegerField(default=0)#0教员1学生
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    createTime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, db_index=True)
    #admin中  ModelAdmin的方法  显示model中字段内容
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    gender = models.CharField(max_length=5)
    types = models.IntegerField(default=1)  # 0教员1学生
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    createTime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, db_index=True)
    def __str__(self):
        return self.name

class TeacherandStudent(models.Model):
    teacher_id = models.ForeignKey("Teacher",on_delete=models.CASCADE)
    student_id = models.ForeignKey("Student",on_delete=models.CASCADE)
    teacher_flag = models.IntegerField(default=0)
    student_flag = models.IntegerField(default=0)
    start_role = models.IntegerField(default=0) #0教员1学生
    createTime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, db_index=True)
    oTime = models.DateTimeField(verbose_name=u'最后时间', auto_now_add=True, db_index=True)