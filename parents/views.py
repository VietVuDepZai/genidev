from django.shortcuts import render,redirect,reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from django.contrib.auth.models import User
#for showing signup/login button for parents
def parentsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'parents/parentsclick.html')

def parents_signup_view(request):
    userForm=forms.parentsUserForm()
    parentsForm=forms.parentsForm()
    mydict={'userForm':userForm,'parentsForm':parentsForm,}
    if request.method=='POST':
        userForm=forms.parentsUserForm(request.POST)
        parentsForm=forms.parentsForm(request.POST,request.FILES)
        if userForm.is_valid() and parentsForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            parents=parentsForm.save(commit=False)
            parents.user=user
            parents.save()
            my_parents_group = Group.objects.get_or_create(name='PARENTS')
            my_parents_group[0].user_set.add(user)
        return HttpResponseRedirect('parentslogin')
    return render(request,'parents/parentssignup.html',context=mydict)



def is_parents(user):
    return user.groups.filter(name='PARENTS').exists()

@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_dashboard_view(request):

    dict={
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count(),
    'parents':models.Parents.objects.get(user=request.user)
    }
    return render(request,'parents/parents_dashboard.html',context=dict)

@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_view_student_marks_view(request):
    name = models.Parents.objects.get(user=request.user)
    return render(request,'parents/parents_view_student_marks.html',{'name':name,     'parents':models.Parents.objects.get(user=request.user)
})

@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_view_marks_view(request,pk):
    courses = QMODEL.Course.objects.all().order_by('-created_at')
    response =  render(request,'parents/parents_view_marks.html',{'courses':courses,'parents':models.Parents.objects.get(user=request.user)})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_check_marks_view(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'parents/parents_check_marks.html',{'results':results,     'parents':models.Parents.objects.get(user=request.user)
})
    
@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'parents/parents_view_exam.html',{'courses':courses,     'parents':models.Parents.objects.get(user=request.user)
})

@login_required(login_url='parentslogin')
def parents_course_view_detail(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.filter(course=course)
    return render(
        request=request,
        template_name='parents/parents_view_course_detail.html',
        context={"course": course,"questions": questions,     'parents':models.Parents.objects.get(user=request.user)}
        )

@login_required(login_url='parentslogin')
def parents_add_blog_view(request):
    context = {'courseForm': QFORM.DocsForm,'parents':models.Parents.objects.get(user=request.user)}
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
            return redirect('/parents/parents-view-blog')
    except Exception as e:
        print(e)

    return render(request, 'parents/parents_add_docs.html', context)

@login_required(login_url='parentslogin')
def delete_blog_view(request,pk):
    course=QMODEL.Docs.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/parents/parents-view-blog')

@login_required(login_url='parentslogin')
def parents_view_blog_view(request):
    courses = QMODEL.Docs.objects.all().order_by('-created_at')
    return render(request,'parents/parents_view_docs.html',{'courses':courses,'parents':models.Parents.objects.get(user=request.user)})


@login_required(login_url="parentslogin")
def updateblog(request, pk):
	course = QMODEL.Docs.objects.get(id=pk)
	form = QFORM.DocsForm(instance=course)
	if request.method == 'POST':
		form = QFORM.DocsForm(request.POST, request.FILES, instance=course)
		if form.is_valid():
			form.save()
		return redirect('/parents/parents-view-docs')

	context = {'courseForm': form, 'parents':models.Parents.objects.get(user=request.user)}
	return render(request, 'parents/parents_update_docs.html', context)

@login_required(login_url='parentslogin')
def parents_view_blog_view_detail(request, pk):
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
        comment_object = models.Comment.objects.create(
            email=email, name=name,
            body=body, post_id=pk
        )
    else:
        comment_form = QFORM.CommentForm()

    context = {'docs':docs,
                'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form,
               'parents':models.Parents.objects.get(user=request.user)}
    return render(request, 'parents/parents_view_docs_detail.html', context) 

def parents_attendance(request):
    return render(request, 'parents/attendance.html', {'attendance': QMODEL.Attendance.objects.filter(user=models.Parents.objects.get(user=request.user).student_model.user).order_by("-id"),'parents':models.Parents.objects.get(user=request.user)})

