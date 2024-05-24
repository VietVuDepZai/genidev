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
path('user-attendance',views.teacher_attendance,name="user-attendance"),
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
# blog
path('teacher-blog', views.teacher_blog_view,name='teacher-blog'),
path('teacher-add-blog', views.teacher_add_blog_view,name='teacher-add-blog'),
path('teacher-view-blog', views.teacher_view_blog_view,name='teacher-view-blog'),
path('delete-blog/<int:pk>', views.delete_blog_view,name='delete-blog'),
path('update-blog/<int:pk>', views.updateblog,name='update-blog'),
path('teacher-view-blog-detail/<int:pk>/', views.teacher_view_blog_view_detail, name="teacher-view-blog-detail"),
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
# Assignments
    path('assignment/',views.assignments,name="assignment"),
    path('add_assign/',views.add_assign,name="add_assign"),
    path('sol_detail_t/<sol_id>', views.sol_detail_t, name='sol_detail_t'),
    path('view_assign/<assign_id>', views.view_assignments, name="view_assign"),
#Quiz
path('listofcourse/',views.view_listofcourse,name="listofcourse"),
path('add_listofcourse/',views.add_listofcourse,name="add_listofcourse"),
path('listofquiz/<int:id>',views.view_listofquiz,name="listofquiz"),
path('add_listofquiz/',views.admin_add_listofquiz,name="add_listofquiz"),
path('update_listofquiz/<int:id>',views.update_listofquiz, name="update_listofquiz"),
path('update_listofcourse/<int:id>',views.update_listofcourse,name="update_listofcourse"),
path('view_listofquiz/<int:id>',views.listofquiz_view_detail,name="view_listofquiz"),
path('delete_listofquiz/<int:id>',views.delete_listofquiz,name="delete_listofquiz"),
path('add_quiz',views.add_quiz,name="add_quiz"),
]