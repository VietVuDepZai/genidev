from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Docs)
admin.site.register(Comment)
admin.site.register(RoomMember)
admin.site.register(Assignment)
admin.site.register(Solution)
admin.site.register(ListOfCourses)
admin.site.register(ListOfQuiz)
admin.site.register(Quiz)
admin.site.register(QuizResult)