from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from django.views.decorators.csrf import csrf_exempt
from quiz import forms as QFORM


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        print("He1")
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            print("He2")
            user.set_password(user.password)
            user.save()
            print("He")
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            print("He")
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
# All subscribe subscribe through "my_group" will get a web push notification.
# A ttl of 1000 is passed so the web push server will store
# the data maximum 1000 seconds if any user is not online

@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    'total_course':QMODEL.Course.objects.all().count(),
    'total_docs':QMODEL.Docs.objects.all().count(),
    'total':  QMODEL.Course.objects.all().count() + QMODEL.Docs.objects.all().count(),
    'student':models.Student.objects.get(user=request.user)
    }
    return render(request,'student/student_dashboard.html',context=dict)

@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all().order_by('-created_at')
    student = models.Student.objects.get(user_id=request.user.id)

    results= QMODEL.Result.objects.all().filter(student=student)
    return render(request,'student/student_exam.html',{'courses':courses, 'results': results,    'student':models.Student.objects.get(user=request.user)
})

@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks,     'student':models.Student.objects.get(user=request.user)
})

@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions,    'student':models.Student.objects.get(user=request.user)
})
    response.set_cookie('course_id',course.id)
    return response

@user_passes_test(is_student)
def student_view_exam_detail(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.filter(course=course)
    return render(
        request=request,
        template_name='student/student_view_exam_detail.html',
        context={"course": course,"questions": questions,     'student':models.Student.objects.get(user=request.user)
}
        )


@user_passes_test(is_student)
@csrf_exempt
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')
        


@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all().order_by('-created_at')
    return render(request,'student/view_result.html',{'courses':courses,    'student':models.Student.objects.get(user=request.user)
})
    

@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course,student=student)
    return render(request,'student/check_marks.html',{'results':results, 'course': course,    'student':models.Student.objects.get(user=request.user)
})

@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all().order_by('-created_at')
    return render(request,'student/student_marks.html',{'courses':courses,    'student':models.Student.objects.get(user=request.user)
})

# Mark
@user_passes_test(is_student)
def student_view_blog_view(request):
    courses = QMODEL.Docs.objects.all().order_by('-created_at')
    return render(request,'student/student_view_docs.html',{'courses':courses,    'student':models.Student.objects.get(user=request.user)
})

@user_passes_test(is_student)
def student_view_blog_view_detail(request, pk):
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
                   'student':models.Student.objects.get(user=request.user)
}
    return render(request, 'student/student_view_docs_view.html', context)


@login_required(login_url='studentlogin')
def student_add_blog_view(request):
    context = {'courseForm': QFORM.DocsForm,'student':models.Student.objects.get(user=request.user)}
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
            return redirect('/student/student-view-blog')
    except Exception as e:
        print(e)

    return render(request, 'student/student_add_docs.html', context)

@login_required(login_url='studentlogin')
def delete_blog_view(request,pk):
    course=QMODEL.Docs.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/student/student-view-blog')

@login_required(login_url="studentlogin")
def updatePost(request, pk):
	course = QMODEL.Docs.objects.get(id=pk)
	form = QFORM.DocsForm(instance=course)
	if request.method == 'POST':
		form = QFORM.DocsForm(request.POST, request.FILES, instance=course)
		if form.is_valid():
			form.save()
		return redirect('/student-view-docs')

	context = {'courseForm': form,'student':models.Student.objects.get(user=request.user)}
	return render(request, 'student/student_update_docs.html', context)

def submit(request,assignment_id):
    assignment=QMODEL.Assignment.objects.get(id=assignment_id)
    student =  models.Student.objects.get(user=request.user)
    form = QFORM.SolutionForm()
    if request.method == 'POST':
        print(request.POST['title'])
        form = QFORM.SolutionForm(data=request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.student = models.Student.objects.get(user=request.user)
            solution.assignment=assignment
            solution.worked=True
            pre_sol=QMODEL.Solution.objects.filter(assignment__id=assignment_id,student=solution.student).all()
            pre_sol.delete()
            solution.save()

            return redirect('')

    else:
        print("###########")
        # print(request.user)
        # usr_year = UserProfile.objects.get(user=request.user).year
        # usr_assign = Assignment.objects.filter(year=usr_year)
        form = QFORM.SolutionForm()
    return render(request, 'quiz/sol_submit.html', {'form': form,'assignment':assignment,'student':models.Student.objects.get(user=request.user)})

def assignments(request):
    return render(request, 'student/assignment.html', {'assignments': QMODEL.Assignment.objects.all().order_by("-id"),'sol': QMODEL.Solution.objects.all().order_by("-id"),'student':models.Student.objects.get(user=request.user)})


def view_assignments(request, assign_id):
    assign = QMODEL.Assignment.objects.get(id=assign_id)
    assign_form = QFORM.AssignmentForm(instance=assign) 
    sol_set = QMODEL.Solution.objects.filter(assignment__id=assign_id)

    return render(request, 'quiz/assignment.html', {'assignment': assign,'sol_set':sol_set,'form':assign_form,'student':models.Student.objects.get(user=request.user)})


def sol_detail_t(request):

    sol_set = QMODEL.Solution.objects.all()

    return render(request, 'student/sol_details_t.html', {'sol_set':sol_set,'student':models.Student.objects.get(user=request.user)})


def detail_t(request,sol_id):
    sol=QMODEL.Solution.objects.get(id=sol_id)
    sol_f = QFORM.SolutionForm(instance=sol)
    form = QFORM.SolCreditForm()
    if request.method=='POST':
        form = QFORM.SolCreditForm(data=request.POST)
        stt=request.POST['comments']
        sol.comments=stt
        sol.points=request.POST['points']
        sol.save()
        return redirect('/student/assignment')


    return render(request,'student/details_t.html',{'sol_f':sol_f, 'sol':sol,'form':form,'student':models.Student.objects.get(user=request.user)})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_listofcourse(request):
    listofcourse  = QMODEL.ListOfCourses.objects.all().order_by("-id")
    return render(request,'student/listofcourse.html',{'listofcourse':listofcourse,'student':models.Student.objects.get(user=request.user)})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_listofquiz(request, id):
    listofcourse  = QMODEL.ListOfCourses.objects.get(id=id)
    listofquiz  = QMODEL.ListOfQuiz.objects.filter(course=listofcourse).order_by("-id")
    return render(request,'student/listofquiz.html',{'courses':listofquiz,'resource':listofcourse,'student':models.Student.objects.get(user=request.user)})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def listofquiz_view_detail(request, id):
    course = QMODEL.ListOfQuiz.objects.get(id=id)
    questions=QMODEL.Quiz.objects.filter(course=course)
    return render(
        request=request,
        template_name='student/student_view_exam_detail.html',
        context={"course": course,"questions": questions,'student':models.Student.objects.get(user=request.user)}
        )

@user_passes_test(is_student)
def take_quiz_view(request,pk):
    course=QMODEL.ListOfQuiz.objects.get(id=pk)
    total_questions=QMODEL.Quiz.objects.all().filter(course=course).count()
    questions=QMODEL.Quiz.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_quiz.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks,     'student':models.Student.objects.get(user=request.user)
})

@user_passes_test(is_student)
def start_quiz_view(request,pk):
    course=QMODEL.ListOfQuiz.objects.get(id=pk)
    questions=QMODEL.Quiz.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_quiz.html',{'course':course,'questions':questions,    'student':models.Student.objects.get(user=request.user)
})
    response.set_cookie('course_id',course.id)
    return response

@user_passes_test(is_student)
def student_view_quiz_detail(request,pk):
    course = QMODEL.ListOfQuiz.objects.get(id=pk)
    questions=QMODEL.Quiz.objects.filter(course=course)
    return render(
        request=request,
        template_name='student/student_view_exam_detail.html',
        context={"course": course,"questions": questions,     'student':models.Student.objects.get(user=request.user)
}
        )


@user_passes_test(is_student)
@csrf_exempt
def calculate_quiz_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.ListOfQuiz.objects.get(id=course_id)
        total_marks=0
        questions=QMODEL.Quiz.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
            # else: 
            #     questions[i].choice = selected_ans
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.QuizResult()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-score')
        


@user_passes_test(is_student)
def view_result_quiz(request):
    courses=QMODEL.ListOfQuiz.objects.all().order_by('-created_at')
    return render(request,'student/view_score.html',{'courses':courses,    'student':models.Student.objects.get(user=request.user)
})
    

@user_passes_test(is_student)
def check_marks_quiz(request,pk):
    course=QMODEL.ListOfQuiz.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.QuizResult.objects.all().filter(exam=course,student=student)
    return render(request,'student/check_quiz.html',{'results':results, 'course': course,    'student':models.Student.objects.get(user=request.user)
})
