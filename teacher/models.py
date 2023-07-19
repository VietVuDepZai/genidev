from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.utils import timezone

# TAG = ((0, "LSĐL"), (1, "Toán"), (2, "Văn"), (3, "Anh"))
CLASS = ((0, "6"), (1, "7"), (2, "8"), (3, "9"))
class Tag(models.Model):
    name = models.CharField(max_length=2000,null=False, default=True)
    def __str__(self):
        return self.name
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    class_model=models.ForeignKey(Tag,on_delete=models.CASCADE,default=True)
    grade=models.IntegerField(choices=CLASS, default=0)
    @property
    def get_name(self):
        self.user.name = self.user.first_name+" "+self.user.last_name 
        return self.user.name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        self.user.name = self.user.first_name+" "+self.user.last_name 
        return self.user.name
    #<iframe allowtransparency=“true” width=“485” height=“402” src="{{}}embed“ frameborder=”0" allowfullscreen></iframe>

class Classroom(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True)
    class_slug = models.SlugField("Class", null=False, blank=False, unique=True)
    content = FroalaField(blank=True, default="")
    notes = FroalaField(blank=True, default="")
    published = models.DateTimeField("Date published", default=timezone.now)
    modified = models.DateTimeField("Date modified", default=timezone.now)
    author = models.ForeignKey(Teacher, default=1, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pic/no_image.jpg', upload_to="profile_pic/" ,max_length=255)

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return self.class_slug

    class Meta:
        verbose_name_plural = "Classroom"
        ordering = ['-published']