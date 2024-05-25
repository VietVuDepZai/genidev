from django.shortcuts import render,redirect,HttpResponse
from . import forms,models
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from parents import models as PMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from parents import forms as PFORM
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quiz.serializers import AttendanceSerializer
from quiz.models import  Attendance
from math import ceil
import base64
import os
import time
import datetime
from json import loads
from _thread import start_new_thread

# Administrators
# def home_view(request):
#     try:
#         return HttpResponseRedirect('/afterlogin')  
#     except: 
#         return render(request,'quiz/index.html')



def home_view(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('afterlogin')  
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			now=datetime.datetime.now()
			if user is not None:
				login(request, user)
				if now.hour<13:
					if now.hour<9:
						data_rec = {'user': user.id, 'date': datetime.datetime.now(),'late':True , 'inout': True}
					else:
						data_rec = {'user': user.id, 'date': datetime.datetime.now(),'late':None , 'inout': True}

				else:
					data_rec = {'user': user.id, 'date': datetime.datetime.now(),'late':None , 'inout': False}
				serializer = AttendanceSerializer(data=data_rec)
				if serializer.is_valid():
					serializer.save()
				return HttpResponseRedirect('afterlogin')
			else:
				pass
		# if request.method == 'GET':
		# 	email = request.GET.get('email')
		return render(request,'quiz/index.html')
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_parents(user):
    return user.groups.filter(name='PARENTS').exists()

# def login_face(request):
#     return render(request,"quiz/login_face.html")

# def recieve_login_face(request):

#     photos = request.POST.getlist('photos[]')
#     paths = []
#     for i, photo in enumerate(photos):
#         ext, img = photo.split(';base64,')
        
#         ext = ext.split('/')[-1]
        
#         name = 'static/temp/rec' + str(i) + '.' + ext
#         fh = open(name, 'wb')
#         fh.write(base64.b64decode(img))
#         fh.close()
#         paths.append('static/temp/rec' + str(i) + '.' + ext)
#     utility.crop_photos(paths=paths)
#     user_id, percentage = face_recognizer.get_image_label(*paths)

#     if user_id in (-1,0, None): 
#         name = 'Unknown'
        
#     else:
#         user = User.objects.get(id=user_id)
#         #manually set the backend attribute
#         user.backend = 'django.contrib.auth.backends.ModelBackend'
#         login(request, user)
#         name= User.objects.get(id=user_id).username
#     now=datetime.datetime.now()
#     if now.hour<13:
#         if now.hour<9:
#             data_rec = {'user': user_id, 'date': datetime.datetime.now(),'late':True , 'inout': True}
#         else:
#             data_rec = {'user': user_id, 'date': datetime.datetime.now(),'late':None , 'inout': True}

#     else:
#         data_rec = {'user': user_id, 'date': datetime.datetime.now(),'late':None , 'inout': False}
#     serializer = AttendanceSerializer(data=data_rec)
#     if serializer.is_valid() and percentage >= 0:
#         serializer.save()
#     return JsonResponse({'id': user_id, 'name': name, 'percentage': percentage})

# def capture_user(request):
#     if is_student(request.user):   
#         accountapproval=SMODEL.Student.objects.all().filter(user_id=request.user.id,status=True)
#         if accountapproval:
#             return HttpResponseRedirect('/student/student-dashboard')
#         else:
#             return render(request,'quiz/capture_signup.html',{'users':accountapproval})
#     if is_parents(request.user):
#         accountapproval=PMODEL.Parents.objects.all().filter(user_id=request.user.id,status=True)
#         if accountapproval:
#             return HttpResponseRedirect('/parents/parents-dashboard')
#         else:
#             return render(request,'quiz/capture_signup.html',{'users':accountapproval})
#     if is_teacher(request.user):
#         accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
#         if accountapproval:
#             return HttpResponseRedirect('/teacher/teacher-dashboard')
#         else:
#             return render(request,'quiz/capture_signup.html',{'users':accountapproval})
#     else:
#         return redirect('admin-dashboard')


def afterlogin_view(request):
    if is_student(request.user):   
        accountapproval=SMODEL.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student/student-dashboard')
        else:
            return render(request,'student/student_wait_for_approval.html')   
    if is_parents(request.user):
        accountapproval=PMODEL.Parents.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('parents/parents-dashboard')
        else:
            return render(request,'parents/parents_wait_for_approval.html')
    if is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def number(request):
    #if test_result is less than 80 execute this
        #twilio code
    client = messagebird.Client("6qz52AzABdmo1J9B3wQfzOtVp")
    message = client.message_create(
        'TestMessage',
        '31687654321',
        'This is a test message',
        { 'reference' : 'Foobar' }
    )
    return render(request,'quiz/send_sms.html')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    'total_parents':PMODEL.Parents.objects.all().count(),
    'total_docs':models.Docs.objects.all().count(),
    'total_class':TMODEL.Classroom.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)
@login_required(login_url='adminlogin')
def admin_user(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'total_parents':PMODEL.Parents.objects.all().count(),
    }
    return render(request,'quiz/admin_users.html',context=dict)
# Teachers
@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'classmodel':TMODEL.Tag.objects.all().count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'quiz/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().order_by("-id")
    return render(request,'quiz/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
def admin_add_teacher_view(request):
    userForm=TFORM.TeacherUserForm()
    teacherForm=TFORM.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm,'content': 'ADD'}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            print(my_teacher_group[0])
            return HttpResponseRedirect('/admin-view-teacher')
    return render(request,'quiz/update_teacher.html',context=mydict)

@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm, 'teacher':teacher, "content":"UPDATE"}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'quiz/update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    teacher.status = True
    teacher.save()
    return HttpResponseRedirect('/admin-view-teacher')

@login_required(login_url='adminlogin')
def approve_parents_view(request,pk):
    teacher=PMODEL.Parents.objects.get(id=pk)
    teacher.status = True
    teacher.save()
    return HttpResponseRedirect('/admin-view-parents')

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher_salary.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
def admin_view_subject(request):
    classmodel = TMODEL.Tag.objects.all()
    return render(request,'quiz/admin_view_subjects.html',{'subjects':classmodel})

@login_required(login_url='adminlogin')
def admin_delete_subject(request, pk):
    subject=TMODEL.Tag.objects.get(id=pk)
    subject.delete()
    return HttpResponseRedirect('/view-subjects')



# Students
@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'courses':models.Course.objects.all()
    }
    return render(request,'quiz/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all().order_by("-id")
    return render(request,'quiz/admin_view_student.html',{'students':students})
    
@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm, "student":student, 'content': 'UPDATE'}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
        return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_add_student_view(request):
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm, 'content': 'ADD'}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=SFORM.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)

@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student') 

@login_required(login_url='adminlogin')
def approve_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm, "student":student, 'content': 'APPROVE'}
    if request.method=='POST':
        student= SMODEL.Student.objects.get(id=pk)
        student.status=True
        student.save()
        return HttpResponseRedirect('/admin-view-student')
    return render(request,'quiz/approve_student.html', context=mydict)
# Parents
@login_required(login_url='adminlogin')
def admin_view_parents_view(request):
    parents= PMODEL.Parents.objects.all().order_by("-id")
    return render(request,'quiz/admin_view_parents.html',{'parents':parents})

@login_required(login_url='adminlogin')
def update_parents_view(request,pk):
    parents=PMODEL.Parents.objects.get(id=pk)
    user=PMODEL.User.objects.get(id=parents.user_id)
    userForm=PFORM.parentsUserForm(instance=user)
    parentsForm=PFORM.parentsForm(request.FILES,instance=parents)
    mydict={'userForm':userForm,'parentsForm':parentsForm,'parents':parents, 'content': 'UPDATE'}
    if request.method=='POST':
        userForm=PFORM.parentsUserForm(request.POST,instance=user)
        parentsForm=PFORM.parentsForm(request.POST,request.FILES,instance=parents)
        if userForm.is_valid() and parentsForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            parentsForm.save()
            return redirect('admin-view-parents')
    return render(request,'quiz/update_parents.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_add_parents_view(request):
    userForm=PFORM.parentsUserForm()
    parentsForm=PFORM.parentsForm()
    mydict={'userForm':userForm,'parentsForm':parentsForm, 'content': 'ADD'}
    if request.method=='POST':
        userForm=PFORM.parentsUserForm(request.POST)
        parentsForm=PFORM.parentsForm(request.POST,request.FILES)
        if userForm.is_valid() and parentsForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            parents=parentsForm.save(commit=False)
            parents.user=user
            parents.save()
            my_parents_group = Group.objects.get_or_create(name='PARENTS')
            my_parents_group[0].user_set.add(user)
            return redirect('admin-view-parents')
    return render(request,'quiz/update_parents.html',context=mydict)

@login_required(login_url='adminlogin')
def delete_parents_view(request,pk):
    parents=PMODEL.Parents.objects.get(id=pk)
    user=User.objects.get(id=parents.user_id)
    user.delete()
    parents.delete()
    return HttpResponseRedirect('/admin-view-parents')



@login_required(login_url='adminlogin')
def admin_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_course.html',{'courses':courses})


@login_required(login_url='adminlogin')
def admin_course_view_detail(request, pk):
    course = models.Course.objects.get(id=pk)
    questions=models.Question.objects.filter(course=course)
    return render(
        request=request,
        template_name='quiz/admin_view_course_detail.html',
        context={"course": course,"questions": questions}
        )


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-course')
    return render(request,'quiz/admin_add_course.html',{'courseForm':courseForm})

@login_required(login_url='adminlogin')
def admin_update_course_view(request, pk):
    course = models.Course.objects.get(id=pk)
    courseForm=forms.CourseForm(instance=course)
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST, instance=course)
        if courseForm.is_valid():        
            courseForm.save()
            return HttpResponseRedirect('/admin-course')
    return render(request,'quiz/admin_update_course.html',{'courseForm':courseForm})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-course')

# Questions

@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'quiz/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            print(course)
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'quiz/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'quiz/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'quiz/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

# Marks
@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'quiz/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'quiz/admin_check_marks.html',{'results':results, 'course':course})
    
# Docs

@login_required(login_url='adminlogin')
def admin_blog_view(request):
    return render(request,'quiz/admin_docs.html')

@login_required(login_url='adminlogin')
def admin_add_blog_view(request):
    context = {'courseForm': forms.DocsForm}
    try:
        if request.method == 'POST':
            form = forms.DocsForm(request.POST)
            title = request.POST.get('title')
            name = request.POST.get('name')

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']  
  
            blog_obj = models.Docs.objects.create(
                title=title, name=name,
                content=content, author=request.user
            )
            print(blog_obj)
            return redirect('/admin-view-blog')
    except Exception as e:
        print(e)

    return render(request, 'quiz/admin_add_docs.html', context)

@login_required(login_url='adminlogin')
def delete_blog_view(request,pk):
    course=models.Docs.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-blog')

@login_required(login_url='adminlogin')
def admin_view_blog_view(request):
    courses = models.Docs.objects.all().order_by('-created_at')
    return render(request,'quiz/admin_view_docs.html',{'courses':courses})


@login_required(login_url="adminlogin")
def updateblog(request, pk):
	course = models.Docs.objects.get(id=pk)
	form = forms.DocsForm(instance=course)
	if request.method == 'POST':
		form = forms.DocsForm(request.POST, request.FILES, instance=course)
		if form.is_valid():
			form.save()
		return redirect('/admin-view-blog')

	context = {'courseForm': form}
	return render(request, 'quiz/admin_update_docs.html', context)

@login_required(login_url='adminlogin')
def admin_view_blog_view_detail(request, pk):
    docs = models.Docs.objects.get(id=pk)
    comments = docs.comments.all()
    new_comment = None
    if request.method == 'POST':
        form = forms.DocsForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            # Create Comment object but don't save to database yet
            # Assign the current post to the comment
            # Save the comment to the database
        comment_object = models.Comment.objects.create(
            email=email, name=name,
            body=body, post_id=pk
        )
    else:
        comment_form = forms.CommentForm()

    context = {'docs':docs,
                'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'quiz/admin_view_docs_detail.html', context) 

# Classroom 
@login_required(login_url='adminlogin')
def admin_view_class_view(request):
    classroom = TMODEL.Classroom.objects.all().order_by('-published')
    return render(request,'quiz/admin_view_class.html',{'classroom':classroom})

@login_required(login_url='adminlogin')
def admin_add_class(request):
    if request.method == "POST":
        form = TFORM.ClassroomCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/admin-class')

    else:
         form =TFORM.ClassroomCreateForm(request.POST, request.FILES)

    return render(
        request=request,
        template_name='quiz/admin_add_class.html',
        context={
            "object": "Classroom",
            "form": form
            }
        )

@login_required(login_url='adminlogin')
def admin_update_class(request, slug):
    # matching_series = TMODEL.Classroom.objects.filter(class_slug=slug).first()
    # form = TFORM.ClassroomCreateForm(instance=matching_series)

    # if request.method == "POST":
    #     form = TFORM.ClassroomCreateForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/admin-class')

    # else:
    #     form =TFORM.ClassroomCreateForm(request.POST, request.FILES)
    matching_series = TMODEL.Classroom.objects.filter(class_slug=slug).first()
    form = TFORM.ClassroomCreateForm(instance=matching_series)
    if request.method == 'POST':
        form = forms.DocsForm(request.POST, request.FILES, instance=matching_series)
        if form.is_valid():
            form.save()
            return redirect('/admin-class')
    else:
        matching_series = TMODEL.Classroom.objects.filter(class_slug=slug).first()
        form = TFORM.ClassroomCreateForm(instance=matching_series)

    return render(
        request=request,
        template_name='quiz/admin_update_class.html',
        context={
            "object": matching_series,
            "form": form
            }
        )

@login_required(login_url='adminlogin')
def admin_view_class_detail(request, slug):
    matching_article = TMODEL.Classroom.objects.filter(class_slug=slug).first()
    
    return render(
        request=request,
        template_name='quiz/admin_view_class_detail.html',
        context={"object": matching_article}
        )

@login_required(login_url='adminlogin')
def delete_class_view(request, slug):
    course=TMODEL.Classroom.objects.filter(class_slug=slug).first() 
    course.delete()
    return HttpResponseRedirect('/admin-view-class')

@login_required(login_url='adminlogin')
def admin_view_student_class(request, slug): 
    room=TMODEL.Classroom.objects.filter(class_slug=slug).first() 
    student = SMODEL.Student.objects.filter(classroom=room).order_by("-id")
    return render(
        request=request,
        template_name='quiz/admin_view_class_student.html',
        context={"object": room, "student": student}
        )



# Create your views here.

def lobby(request):
    if request.user.is_authenticated:   
        return render(request, 'videocall/lobby.html')
    else: 
        return HttpResponseRedirect("/afterlogin")

def room(request):
    if request.user.is_authenticated:   
        if request.method == 'POST':
            roomID = request.POST['roomID']
            return redirect("/meeting?roomID=" + roomID)
        return render(request, 'videocall/room.html')
    else: 
        return HttpResponseRedirect("/afterlogin")


def getToken(request):
    appId = "a3195752a2b349398296e70fe3e0acdc"
    appCertificate = "6b4b6870da3444db86983c66df8f6800"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):  
    members = RoomMember.objects.get(uid=json.loads(request.body)['UID'])
    members.delete()
    return  HttpResponseRedirect("/meeting")

# Footer


def aboutus_view(request):
    return render(request,'quiz/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail('Title: '+str(name)+' || '+'Email: '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form':sub})

def comingsoon(request):
    return render(request,'quiz/comingsoon.html')

#!/usr/bin/env python3


@login_required(login_url='adminlogin')
def home(request):

    return render(request, "recognition/home.html",
                  {'photos': trainer.get_nbr_photos(),
                   'users': User.objects.count(),
                   'last_training': utility.last_training()}, )

@login_required(login_url='adminlogin')
def about(request):

    return render(request, 'recognition/about.html', {})


@login_required(login_url='adminlogin')
def capture(request):

    if User.objects.count() == 0:
        return redirect('/adduser/?status=empty')
    return render(request, 'recognition/capture.html', {'users': User.objects.all()})

@login_required(login_url='adminlogin')
def display_users(request):

    return render(request, 'recognition/user.html', {'users': User.objects.all()})


def train(request):

    if not utility.are_there_photos():
        return redirect('/capture/?status=empty')
    return render(request, 'recognition/train.html')




def receive_images(request):
    label = request.POST.get('label')
    photos = request.POST.getlist('photos[]')
    start_new_thread(utility.save_base64_photos, (label, photos))
    return HttpResponse()


def receive_train(request):

    start = time.time()
    trainer.train()
    start_new_thread(face_recognizer.reload, ())
    duration = ceil(time.time() - start)
    return JsonResponse({'duration': duration})


def profile(request, id=1):

    user_data = User.objects.get(pk=id)
    images = [filename for filename in os.listdir(photos_path) if filename.split('_')[0] == str(id)]
    return render(request, 'recognition/profile.html', {'user': user_data, 'images': images})


def delete_user(request):

    user_id = request.POST.get('id')
    User.objects.filter(id=user_id).delete()
    Attendance.objects.filter(id=user_id).delete()
    images = [filename for filename in os.listdir(photos_path) if filename.split('_')[0] == str(id)]
    for image in images:
        os.remove('static/photos/' + image)
    return HttpResponse()


def recognize_camera(request):

    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    return render(request, 'recognition/camera.html')


def receive_recognize(request):

    photos = request.POST.getlist('photos[]')
    paths = []
    for i, photo in enumerate(photos):
        ext, img = photo.split(';base64,')
        
        ext = ext.split('/')[-1]
        
        name = 'static/temp/rec' + str(i) + '.' + ext
        fh = open(name, 'wb')
        fh.write(base64.b64decode(img))
        fh.close()
        paths.append('static/temp/rec' + str(i) + '.' + ext)
    utility.crop_photos(paths=paths)
    user_id, percentage = face_recognizer.get_image_label(*paths)
    
    if user_id in (-1,0, None): 
        name = 'Unknown'
        
    else:
        name= User.objects.get(id=user_id).username
    now=datetime.datetime.now()
    if now.hour<13:
        if now.hour<9:
            data_rec = {'user': user_id, 'date': datetime.datetime.now(),'late':True , 'inout': True}
        else:
            data_rec = {'user': user_id, 'date': datetime.datetime.now(),'late':None , 'inout': True}

    else:
        data_rec = {'user': user_id, 'date': datetime.datetime.now(),'late':None , 'inout': False}
    serializer = AttendanceSerializer(data=data_rec)
    if serializer.is_valid() and percentage >= 0:
        serializer.save()
    return JsonResponse({'id': user_id, 'name': name, 'percentage': percentage})


def recognize_photo(request):

    if not utility.is_model_trained():
        return redirect('/train/?status=untrained')
    return render(request, 'recognition/recognise_photo.html')


def view_photos(request):

    users = User.objects.all()
    data = []
    for user in users:
        images = [filename for filename in os.listdir(photos_path) if filename.split('_')[0] == str(user.id)]
        data.append({'user': user.username, 'images': images})
    return render(request, 'recognition/viewPhoto.html', {'data': data})




class AttendanceRecord(APIView):
    def post(self, request, format=None):
        data = loads(request.body)
        operation = int(data['operation'])
        if operation == 100:  # Sent images to recognize
            date = datetime.datetime.fromtimestamp(int(data['date']))
            if date.hour <= 13:
                inout = True

                if date.hour<=9:
                        late = None
                else:
                        late = True
        
            else:
                inout=False
                late= None

            paths = []
            for i, photo in enumerate(data['images']):
                name = 'static/temp/rec' + str(i) + '.png'
                with open(name, 'wb') as fh:
                    fh.write(base64.b64decode(photo))
                paths.append(name)

        elif operation == 200:  # Remote capture photos
            date = datetime.datetime.now()
            paths = utility.remote_capture(3)
            inout = None

        utility.crop_photos(paths=paths)
        user_id, percentage = face_recognizer.get_image_label(*paths)
        if user_id not in (-1, None) and percentage > 0:
            data_rec = {'user': user_id, 'date': date, 'late': late,'inout': inout}
            serializer = AttendanceSerializer(data=data_rec)
            if serializer.is_valid():
                # Add DB records
                serializer.save()
                inout = Attendance.objects.last().inout
                print("----------------")
                print(inout)
                # Run assigned tasks
                #tasks.do_user_tasks(user_id, inout=inout)
                # Save captured images for future training
                # utility.add_new_user_photos(user=user_id, path=paths[0])
                user = User.objects.get(id=user_id)
                json_data = {'user': user.first_name + ' ' + user.last_name, 'department':user.department,'late':late,'inout': inout}
                return JsonResponse(json_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


def attendance(request):

    return render(request, 'recognition/attendance.html', {'attendance': Attendance.objects.all().order_by("-id")})

def quiz_attendance(request):

    return render(request, 'quiz/attendance.html', {'attendance': Attendance.objects.all().order_by("-id")})


@login_required(login_url='adminlogin')
def assignments(request):
    return render(request, 'quiz/assignments.html', {'assignments': models.Assignment.objects.all().order_by("-id")})

@login_required(login_url='adminlogin')
def view_assignments(request, assign_id):
    assign = models.Assignment.objects.get(id=assign_id)
    assign_form = forms.AssignmentForm(instance=assign) 
    sol_set = models.Solution.objects.filter(assignment__id=assign_id)

    return render(request, 'quiz/details_t.html', {'assignment': assign,'sol_set':sol_set,'form':assign_form})

@login_required(login_url='adminlogin')
def add_assign(request):
    form = forms.AssignmentForm()

    if request.method == 'POST':
        form = forms.AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/assignment')

    else:
        # print(request.user)
        # usr_year = UserProfile.objects.get(user=request.user).year
        # usr_assign = Assignment.objects.filter(year=usr_year)
        form = forms.AssignmentForm()
    return render(request, 'quiz/add_assign.html', {'form': form})

@login_required(login_url='adminlogin')
def sol_detail_t(request,sol_id):
    sol=models.Solution.objects.get(id=sol_id)
    sol_f = forms.SolutionForm(instance=sol)
    form = forms.SolCreditForm()
    if request.method=='POST':
        form = forms.SolCreditForm(data=request.POST)
        stt=request.POST['comments']
        sol.comments=stt
        sol.points=request.POST['points']
        sol.save()
        return redirect('/assignment')


    return render(request,'quiz/sol_details_t.html',{'sol_f':sol_f, 'sol':sol,'form':form})

@login_required(login_url='adminlogin')
def view_listofcourse(request):
    listofcourse  = models.ListOfCourses.objects.all().order_by("-id")
    return render(request,'quiz/listofcourse.html',{'listofcourse':listofcourse})

@login_required(login_url='adminlogin')
def add_listofcourse(request):
    form =forms.ListOfCourse()
    if request.method == "POST":
        form = forms.ListOfCourse(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listofcourse')
        else:
            return redirect('/add_listofcourse')
   

    return render(request,'quiz/add_listofcourse.html',{'form':form})

@login_required(login_url='adminlogin')
def update_listofcourse(request,id):
    course = models.ListOfCourses.objects.get(id=id)
    form =forms.ListOfCourse(instance=course)
    if request.method == "POST":
        form = forms.ListOfCourse(request.POST, request.FILES,instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listofcourse')
        else:
            return redirect('/update_listofcourse')
   

    return render(request,'quiz/update_listofcourse.html',{'form':form})


@login_required(login_url='adminlogin')
def delete_listofcourse(request, id):    
    course=models.ListOfCourses.objects.get(id=id)
    course.delete()
    return HttpResponseRedirect('/listofcourse/')

@login_required(login_url='adminlogin')
def view_listofquiz(request, id):
    listofcourse  = models.ListOfCourses.objects.get(id=id)
    listofquiz  = models.ListOfQuiz.objects.filter(course=listofcourse).order_by("-id")
    return render(request,'quiz/listofquiz.html',{'courses':listofquiz,'resource':listofcourse})

@login_required(login_url='adminlogin')
def admin_add_listofquiz(request):
    courseForm=forms.ListOfQuiz()
    if request.method=='POST':
        courseForm=forms.ListOfQuiz(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/listofcourse')
    return render(request,'quiz/add_listofquiz.html',{'courseForm':courseForm})

@login_required(login_url='adminlogin')
def update_listofquiz(request, id):
    course = models.ListOfQuiz.objects.get(id=id)
    courseForm=forms.ListOfQuiz(instance=course)
    if request.method=='POST':
        courseForm=forms.ListOfQuiz(request.POST,instance=course)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/listofcourse')
    return render(request,'quiz/update_listofquiz.html',{'courseForm':courseForm})

@login_required(login_url='adminlogin')
def listofquiz_view_detail(request, id):
    course = models.ListOfQuiz.objects.get(id=id)
    questions=models.Quiz.objects.filter(course=course)
    return render(
        request=request,
        template_name='quiz/admin_view_course_detail.html',
        context={"course": course,"questions": questions}
        )

@login_required(login_url='adminlogin')
def delete_listofquiz(request, id):    
    course=models.ListOfQuiz.objects.get(id=id)
    course.delete()
    return HttpResponseRedirect(f'/listofquiz/{id}')


@login_required(login_url='adminlogin')
def add_quiz(request):
    questionForm=forms.Quiz()
    if request.method=='POST':
        questionForm=forms.Quiz(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            id = question.course.id
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect(f'/view_listofquiz/{id}')
    return render(request,'quiz/add_quiz.html',{'questionForm':questionForm})

@login_required(login_url='adminlogin')
def update_quiz(request, id):
    question = models.Quiz.objects.get(id=id)
    questionForm=forms.Quiz()
    if request.method=='POST':
        questionForm=forms.Quiz(request.POST, instance=question)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            id = question.course.id
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect(f'/view_listofquiz/{id}')
    return render(request,'quiz/add_quiz.html',{'questionForm':questionForm})
