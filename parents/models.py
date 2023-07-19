from django.db import models
from django.contrib.auth.models import User
from student.models import Student
class Parents(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    student_model = models.ForeignKey(Student,on_delete=models.CASCADE,default=True)
    @property
    def get_name(self):
        self.user.name = self.user.first_name+" "+self.user.last_name+" "+self.student_model
        return self.user.name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        self.user.name = self.user.first_name+" "+self.user.last_name +" "+str(self.student_model)
        return self.user.name