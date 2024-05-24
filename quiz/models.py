from django.db import models
from teacher import models as TMODEL
from student.models import Student
from teacher.models import Teacher
from django.db.models import Sum
from froala_editor.fields import FroalaField
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class ListOfCourses(models.Model):
    name = models.CharField(max_length=500)
    icon = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    deadline = models.DateField()
    classroom = models.ForeignKey(TMODEL.Classroom,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name 
    def autodelete(self):   
        if str(self.deadline)[0:10] == str(timezone.now())[0:10]: 
            return True
        else: 
            return False

    def save(self):
        super(ListOfCourses, self).save()
                
class ListOfQuiz(models.Model):
    course = models.ForeignKey(ListOfCourses, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=500)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    atempt = models.PositiveIntegerField(default=2)
    date = models.DateTimeField()
    limited_mins = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    close = False   
    def __str__(self):
        return self.course_name 
    def autodelete(self):
        print(str(self.date)[0:10])
        print(str(timezone.now())[0:10])
        # print(now)
        if str(self.date)[0:10] == str(timezone.now())[0:10]: 
            self.close = True
            return self.close
        else: 
            return self.close
    class Meta:
        ordering = ['-created_at']


class Quiz(models.Model):
    course=models.ForeignKey(ListOfQuiz,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600) # Mai mốt chuyển hết sang FroalaField
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    choice=models.CharField(max_length=200, blank=True, null=True)
    answer=models.CharField(max_length=200,choices=cat)

class Course(models.Model):
    course_name = models.CharField(max_length=500)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    atempt = models.PositiveIntegerField(default=2)
    date = models.DateTimeField()
    limited_mins = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    close = False   
    def __str__(self):
        return self.course_name 
    def autodelete(self):
        print(str(self.date)[0:10])
        print(str(timezone.now())[0:10])
        # print(now)
        if str(self.date)[0:10] == str(timezone.now())[0:10]: 
            self.close = True
            return self.close
        else: 
            return self.close
    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600) # Mai mốt chuyển hết sang FroalaField
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Assignment(models.Model):
	YEAR_IN_COLLEGE_CHOICES = (
		(1, 'Grade 6'),
		(2, 'Grade 7'),
		(3, 'Grade 8'),
		(4, 'Grade 9'),
	)

	classroom=models.ForeignKey(TMODEL.Classroom,on_delete=models.CASCADE,null=True,blank=True)
	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	year = models.IntegerField(choices=YEAR_IN_COLLEGE_CHOICES, default=1)
	name = models.CharField(max_length = 200)
	questions = FroalaField()
	num=models.IntegerField(default=1)
	created = models.DateField(editable=False, null=True)
	updated = models.DateTimeField(editable=False, null=True)
	deadline = models.DateField()
	img = models.ImageField(upload_to='assign/',null=True,blank=True)
	def __str__(self):
		return self.name

	def save(self):
		if not self.id:
			self.created = datetime.date.today()
		self.updated = datetime.datetime.today()
		super(Assignment, self).save()
                
	def autodelete(self):   
		if str(self.deadline)[0:10] == str(timezone.now())[0:10]: 
			return True
		else: 
			return False
                
class Solution(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
	submission_date = models.DateField()
	title=models.CharField(max_length=100,default="")
	body=FroalaField()
	points=models.FloatField(default=0.)
	comments=models.CharField(max_length=200,default="")
	worked=models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def save(self):
		self.submission_date = datetime.date.today()
		super(Solution, self).save()


class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


class QuizResult(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(ListOfQuiz,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


class Docs(models.Model):
    title = models.CharField(max_length=100,  default="Hướng dẫn sử dụng GeniDev")
    content = FroalaField()
    slug = models.SlugField(max_length=200,  default="huongdansudung")
    name = models.CharField(max_length=1000,  default="Hướng dẫn sử dụng GeniDev để phục vụ học tập")
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.title

    def isnumeric(self):
        name = self.name
        if name.isnumeric() is True:
            return True
        else:
            return False
    def save(self, *args, **kwargs):
        super(Docs, self).save(*args, **kwargs)
    class Meta:
        ordering = ['created_at']
class Comment(models.Model):
    post = models.ForeignKey(Docs,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    id = models.AutoField(name='id', primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    date = models.DateTimeField()
    late = models.BooleanField(null=True)
    inout = models.BooleanField(null=True)

