from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from student import forms as SFORM
from parents import models as PMODEL
from parents import forms as PFORM
from quiz import forms as QFORM
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
import json
from django.views.decorators.csrf import csrf_exempt
#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
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
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    'pending_parents':PMODEL.Parents.objects.all().filter(status=False).count(),
    'pending_student':SMODEL.Student.objects.all().filter(status=False).count(),
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count(),
    'total_parent':PMODEL.Parents.objects.all().count(),
    'teacher': models.Teacher.objects.get(user=request.user)
    }

    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html', {'teacher': models.Teacher.objects.get(user=request.user)})



@login_required(login_url='teacherlogin')
def teacher_student_view(request):
    dict={
    'students':SMODEL.Student.objects.all(),
    'teacher': models.Teacher.objects.get(user=request.user)
    }
    return render(request,'teacher/teacher_student.html',context=dict)

    
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm, "student":student, 'content': 'UPDATE','teacher': models.Teacher.objects.get(user=request.user)}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'teacher/update_student.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def add_student_view(request):
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm, 'content': 'ADD','teacher': models.Teacher.objects.get(user=request.user)}
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
    return render(request,'teacher/update_student.html',context=mydict)

@login_required(login_url='teacherlogin')
def teacher_parents_view(request):
    dict={
    'parents':PMODEL.Parents.objects.all(),
    'teacher': models.Teacher.objects.get(user=request.user)
    }
    return render(request,'teacher/teacher_parents.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def teacher_view_exam_detail(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.filter(course=course)
    return render(
        request=request,
        template_name='teacher/teacher_view_exam_detail.html',
        context={"course": course,"questions": questions, 'teacher': models.Teacher.objects.get(user=request.user)}
        )

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all().order_by('-created_at')
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses , 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def teacher_update_course_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    courseForm=QFORM.CourseForm(instance=course)
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST, instance=course)
        if courseForm.is_valid():        
            courseForm.save()
            return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_update_course.html',{'courseForm':courseForm, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='teacherlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html',  {'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.all().order_by('-created_at')
    return render(request,'teacher/teacher_view_question.html',{'courses':courses,'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().order_by('-created_at').filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

# approve parents
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_pending_parents_view(request):
    parents= PMODEL.Parents.objects.all().filter(status=False).order_by("_id")
    return render(request,'teacher/teacher_pending_parents.html',{'parents':parents, 'teacher': models.Teacher.objects.get(user=request.user)})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def approve_parents_view(request,pk):
    parents= PMODEL.Parents.objects.get(id=pk)
    if request.method=='POST':
        parents= PMODEL.Parents.objects.get(id=pk)
        parents.status=True
        parents.save()
        return HttpResponseRedirect('/teacher/teacher-view-parents')
    return render(request,'teacher/check_parents.html',  { 'parents':parents, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def reject_parents_view(request,pk):
    parents= PMODEL.Parents.objects.get(id=pk)
    user=models.User.objects.get(id=parents.user_id)
    user.delete()
    parents.delete()
    return HttpResponseRedirect('/teacher/teacher-view-parents')
# approve student
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_pending_student_view(request):
    student= SMODEL.Student.objects.all().filter(status=False)
    return render(request,'teacher/teacher_pending_student.html',{'student':student,  'teacher': models.Teacher.objects.get(user=request.user)})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def approve_student_view(request,pk):
    student= SMODEL.Student.objects.get(id=pk)

    if request.method=='POST':
        student= SMODEL.Student.objects.get(id=pk)
        student.status=True
        student.save()
        return HttpResponseRedirect('/teacher/teacher-view-student')
    return render(request,'teacher/check_student.html',  {'student':student,'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def reject_student_view(request,pk):
    student= SMODEL.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/teacher/teacher-view-student')
# Docs
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_blog_view(request):
    return render(request,'teacher/teacher_view_docs.html', {'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_blog_view(request):
    context = {'courseForm': QFORM.DocsForm,  'teacher': models.Teacher.objects.get(user=request.user)}
    try:
        if request.method == 'POST':
            form = QFORM.DocsForm(request.POST)
            title = request.POST.get('title')
            name = request.POST.get('name')

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']  
  
            blog_obj = QMODEL.Docs.objects.create(
                title=title, name=name,
                content=content, author=request.user
            )
            print(blog_obj)
            return redirect('/teacher/teacher-view-blog')
    except Exception as e:
        print(e)

    return render(request, 'teacher/teacher_add_docs.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_blog_view(request,pk):
    course=QMODEL.Docs.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-blog')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_blog_view(request):
    docs = QMODEL.Docs.objects.all().order_by('-created_at')
    return render(request,'teacher/teacher_view_docs.html',{'docs':docs,  'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url="teacherlogin")
def updateblog(request, pk):
	course = QMODEL.Docs.objects.get(id=pk)
	form = QFORM.DocsForm(instance=course)
	if request.method == 'POST':
		form = QFORM.DocsForm(request.POST, request.FILES, instance=course)
		if form.is_valid():
			form.save()
		return redirect('/teacher/teacher-view-blog')

	context = {'courseForm': form,  'teacher': models.Teacher.objects.get(user=request.user)}
	return render(request, 'teacher/teacher_update_docs.html', context)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_blog_view_detail(request, pk):
    docs = QMODEL.Docs.objects.get(id=pk)
    comments = docs.comments.all()
    new_comment = None
    if request.method == 'POST':
        form = QFORM.DocsForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_form = QFORM.CommentForm(data=request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            # Create Comment object but don't save to database yet
            # Assign the current post to the comment
            # Save the comment to the database
        comment_object = QMODEL.Comment.objects.create(
            email=email, name=name,
            body=body, post_id=pk
        )
    else:
        comment_form = QFORM.CommentForm()

    context = {'docs':docs,
                'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form,
                'teacher': models.Teacher.objects.get(user=request.user)}
    return render(request, 'teacher/teacher_view_docs_view.html', context)
# Marks
@login_required(login_url='teacherlogin')
def teacher_view_student_marks_view(request):
    teacher = models.Teacher.objects.get(user=request.user)
    matching_article =  models.Classroom.objects.get(author=teacher)
    students = SMODEL.Student.objects.filter(classroom=matching_article).order_by("-id")

    return render(request,'teacher/teacher_view_student_marks.html',{'students':students, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def teacher_view_marks_view(request,pk):
    courses = QMODEL.Course.objects.all().order_by('-created_at')
    response =  render(request,'teacher/teacher_view_marks.html',{'courses':courses,'teacher': models.Teacher.objects.get(user=request.user)})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='teacherlogin')
def teacher_check_marks_view(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'teacher/teacher_check_marks.html',{'results':results, 'course':course, 'teacher': models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_class_view(request):
    teacher = models.Teacher.objects.get(user=request.user)
    matching_article =  models.Classroom.objects.get(author=teacher)
    form = forms.ClassroomCreateForm(instance=matching_article)
    return render(
        request=request,
        template_name='teacher/teacher_view_class.html',
        context={"object": matching_article,  'teacher': teacher, 'form':form,'teacher': models.Teacher.objects.get(user=request.user)}
        )

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_update_class(request, slug):
    # matching_series = models.Classroom.objects.filter(class_slug=slug).first()
    # form = forms.ClassroomCreateForm(instance=matching_series)

    # if request.method == "POST":
    #     form = forms.ClassroomCreateForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/teacher-class')

    # else:
    #     form =forms.ClassroomCreateForm(request.POST, request.FILES)
    matching_series = models.Classroom.objects.filter(class_slug=slug).first()
    form = forms.ClassroomCreateForm(instance=matching_series)
    if request.method == 'POST':
        form = forms.DocsForm(request.POST, request.FILES, instance=matching_series)
        if form.is_valid():
            form.save()
            return redirect('/teacher-class')
    else:
        matching_series = models.Classroom.objects.filter(class_slug=slug).first()
        form = forms.ClassroomCreateForm(instance=matching_series)

    return render(
        request=request,
        template_name='teacher/teacher_update_class.html',
        context={
            "object": matching_series,
            "form": form,
            'teacher': models.Teacher.objects.get(user=request.user)
            }
        )

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_class(request, slug): 
    room=models.Classroom.objects.filter(class_slug=slug).first() 
    student = SMODEL.Student.objects.filter(classroom=room).order_by("-id")
    return render(
        request=request,
        template_name='teacher/teacher_view_class_student.html',
        context={"object": room, "student": student,'teacher': models.Teacher.objects.get(user=request.user)}
        )

def teacher_attendance(request):
    room=models.Classroom.objects.get(author=models.Teacher.objects.get(user=request.user))

    student = SMODEL.Student.objects.filter(classroom=room).order_by("-id")

    return render(request, 'teacher/attendance.html', {'attendance': QMODEL.Attendance.objects.filter(user=SMODEL.Student.objects.get(classroom=room).user),'teacher':models.Teacher.objects.get(user=request.user)})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def view_listofcourse(request):
    listofcourse  = QMODEL.ListOfCourses.objects.all().order_by("-id")
    return render(request,'teacher/listofcourse.html',{'listofcourse':listofcourse,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def add_listofcourse(request):
    form =QFORM.ListOfCourse()
    if request.method == "POST":
        form = QFORM.ListOfCourse(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teacher/listofcourse')
        else:
            return redirect('/teacher/add_listofcourse')
   

    return render(request,'teacher/add_listofcourse.html',{'form':form,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_listofcourse(request,id):
    course = QMODEL.ListOfCourses.objects.get(id=id)
    form =QFORM.ListOfCourse(instance=course)
    if request.method == "POST":
        form = QFORM.ListOfCourse(request.POST, request.FILES,instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teacher/listofcourse')
        else:
            return redirect('/teacher/update_listofcourse')
   

    return render(request,'teacher/update_listofcourse.html',{'form':form,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def view_listofquiz(request, id):
    listofcourse  = QMODEL.ListOfCourses.objects.get(id=id)
    listofquiz  = QMODEL.ListOfQuiz.objects.filter(course=listofcourse).order_by("-id")
    return render(request,'teacher/listofquiz.html',{'courses':listofquiz,'resource':listofcourse,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def admin_add_listofquiz(request):
    courseForm=QFORM.ListOfQuiz()
    if request.method=='POST':
        courseForm=QFORM.ListOfQuiz(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/listofcourse')
    return render(request,'teacher/add_listofquiz.html',{'courseForm':courseForm,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_listofquiz(request, id):
    course = QMODEL.ListOfQuiz.objects.get(id=id)
    courseForm=QFORM.ListOfQuiz(instance=course)
    if request.method=='POST':
        courseForm=QFORM.ListOfQuiz(request.POST,instance=course)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/listofcourse')
    return render(request,'teacher/update_listofquiz.html',{'courseForm':courseForm,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def listofquiz_view_detail(request, id):
    course = QMODEL.ListOfQuiz.objects.get(id=id)
    questions=QMODEL.Quiz.objects.filter(course=course)
    return render(
        request=request,
        template_name='teacher/teacher_view_exam_detail.html',
        context={"course": course,"questions": questions,'teacher':models.Teacher.objects.get(user=request.user)}
        )

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_listofquiz(request, id):    
    course=QMODEL.ListOfQuiz.objects.get(id=id)
    course.delete()
    return HttpResponseRedirect(f'/teacher/listofquiz/{id}')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def add_quiz(request):
    questionForm=QFORM.Quiz()
    if request.method=='POST':
        questionForm=QFORM.Quiz(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            id = request.POST.get('courseID')
            course=QMODEL.ListOfQuiz.objects.get(id=id)
            print(course)
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect(f'/teacher/view_listofquiz/{id}')
    return render(request,'teacher/add_quiz.html',{'questionForm':questionForm,'teacher':models.Teacher.objects.get(user=request.user)})


@login_required(login_url='teacherlogin')
def assignments(request):
    return render(request, 'teacher/assignments.html', {'assignments': QMODEL.Assignment.objects.all().order_by("-id"),'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def view_assignments(request, assign_id):
    assign = QMODEL.Assignment.objects.get(id=assign_id)
    assign_form = QFORM.AssignmentForm(instance=assign) 
    sol_set = QMODEL.Solution.objects.filter(assignment__id=assign_id)

    return render(request, 'teacher/details_t.html', {'assignment': assign,'sol_set':sol_set,'form':assign_form})

@login_required(login_url='teacherlogin')
def add_assign(request):
    form = QFORM.AssignmentForm()

    if request.method == 'POST':
        form = QFORM.AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/assignment')

    else:
        # print(request.user)
        # usr_year = UserProfile.objects.get(user=request.user).year
        # usr_assign = Assignment.objects.filter(year=usr_year)
        form = QFORM.AssignmentForm()
    return render(request, 'teacher/add_assign.html', {'form': form})

@login_required(login_url='teacherlogin')
def sol_detail_t(request,sol_id):
    sol=QMODEL.Solution.objects.get(id=sol_id)
    sol_f = QFORM.SolutionForm(instance=sol)
    form = QFORM.SolCreditForm()
    if request.method=='POST':
        form = QFORM.SolCreditForm(data=request.POST)
        stt=request.POST['comments']
        sol.comments=stt
        sol.points=request.POST['points']
        sol.save()
        return redirect('/assignment')


    return render(request,'quiz/sol_details_t.html',{'sol_f':sol_f, 'sol':sol,'form':form})
@login_required(login_url='teacherlogin')
def update_quiz(request, id):
    question = QMODEL.Quiz.objects.get(id=id)
    questionForm=QFORM.Quiz(instance=question)
    if request.method=='POST':
        questionForm=QFORM.Quiz(request.POST, instance=question)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            id = question.course.id
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect(f'/teacher/view_listofquiz/{id}')
    return render(request,'teacher/update_quiz.html',{'questionForm':questionForm,'teacher':models.Teacher.objects.get(user=request.user)})

@login_required(login_url='teacherlogin')
def delete_quiz(request,pk):
    question = QMODEL.Quiz.objects.get(id=pk)
    id = question.course.id
    question.delete()
    return HttpResponseRedirect(f'/teacher/view_listofquiz/{id}')