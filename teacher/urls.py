from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
# Teachers
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
# Exams
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),
path('update-exam/<int:pk>', views.teacher_update_course_view, name="update-exam"),
path('view-exam/<int:pk>', views.teacher_view_exam_detail, name="view-exam"),
# Questions
path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
# Docs
path('teacher-docs', views.teacher_docs_view,name='teacher-docs'),
path('teacher-add-docs', views.teacher_add_docs_view,name='teacher-add-docs'),
path('teacher-view-docs', views.teacher_view_docs_view,name='teacher-view-docs'),
path('delete-docs/<int:pk>', views.delete_docs_view,name='delete-docs'),
path('teacher-view-docs-detail/<int:pk>/', views.teacher_view_docs_view_detail, name="teacher-view-docs-detail"),
# Parents
path('teacher-view-pending-parents', views.teacher_view_pending_parents_view,name='teacher-view-pending-parents'),
path('approve-parents/<int:pk>', views.approve_parents_view,name='approve-parents'),
path('reject-parents/<int:pk>', views.reject_parents_view,name='reject-parents'),
path('teacher-view-parents', views.teacher_parents_view, name="teacher-view-parents"),
# Students
path('teacher-view-pending-student', views.teacher_view_pending_student_view,name='teacher-view-pending-student'),
path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
path('reject-student/<int:pk>', views.reject_student_view,name='reject-student'),
path('teacher-view-student', views.teacher_student_view, name="teacher-view-student"),
path('teacher-add-student', views.add_student_view,name='teacher-add-student'),
path('update-student/<int:pk>', views.update_student_view,name='update-student'),
# Marks
path('teacher-view-student-marks', views.teacher_view_student_marks_view,name='teacher-view-student-marks'),
path('teacher-view-marks/<int:pk>', views.teacher_view_marks_view,name='teacher-view-marks'),
path('teacher-check-marks/<int:pk>', views.teacher_check_marks_view,name='teacher-check-marks'),
# Class room
path('teacher-class', views.teacher_view_class_view,  name="teacher-class"),
path("teacher-update-class/<slug>", views.teacher_update_class, name="teacher-update-class"),
path("teacher-view-class-student/<slug>", views.teacher_view_student_class, name="teacher-view-class-student"),

# # Online room
# path('meeting', views.lobby),
# path('room/', views.room),
# path('get_token/', views.getToken),
# path('create_member/', views.createMember),
# path('get_member/', views.getMember),
# path('delete_member/', views.deleteMember),

]