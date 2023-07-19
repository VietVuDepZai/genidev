from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from froala_editor.fields import FroalaField


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class SolutionForm(forms.ModelForm):
    body = FroalaField()
    class Meta:
        model = models.Solution
        fields = ['title','body']


class CourseForm(forms.ModelForm):
    date = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks','atempt','date','limited_mins']
        


class QuestionForm(forms.ModelForm):
    
    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class DocsForm(forms.ModelForm):
    class Meta:
        model=models.Docs
        fields=['title','name','content','slug']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['name', 'email', 'body']


class AssignmentForm(forms.ModelForm):
    deadline = forms.DateField(widget=AdminDateWidget())
    course=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Assignment
        fields=['name','questions','deadline','year','teacher','img']

class SolCreditForm(forms.ModelForm):
	class Meta:
		model=models.Solution
		fields=['points','comments']
                
class ListOfCourse(forms.ModelForm):
    deadline = forms.DateField(widget=AdminDateWidget())
    class Meta:
        model=models.ListOfCourses
        fields = '__all__'

class ListOfQuiz(forms.ModelForm):
    date = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    course=forms.ModelChoiceField(queryset=models.ListOfCourses.objects.all().order_by("-id"),empty_label="Resource Name", to_field_name="id")

    class Meta:
        model=models.ListOfQuiz
        fields=['course','course_name','question_number','total_marks','atempt','date','limited_mins']


class Quiz(forms.ModelForm):
    
    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    course=forms.ModelChoiceField(queryset=models.ListOfQuiz.objects.all().order_by("-id"),empty_label="Resource Name", to_field_name="id")
    class Meta:
        model=models.Quiz
        fields=['course','marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }