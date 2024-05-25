from django.urls import path,include,re_path
from django.contrib import admin
from quiz import views
from django.contrib.auth.views import LogoutView,LoginView
from django.views.static import serve
from django.conf import settings
from django.views.i18n import JavaScriptCatalog
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Apps
    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path('parents/',include('parents.urls')),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # Homepages
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='quiz/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('comingsoon', views.comingsoon,name='comingsoon'),
    # Admin views
    path('adminusers', views.admin_user,name='adminusers'),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='quiz/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    # Admin teachers
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),
    path('view-subjects', views.admin_view_subject, name="view-subjects"),
    path('admin-add-teacher', views.admin_add_teacher_view, name="admin-add-teacher"),
    path('delete-subject/<int:pk>', views.admin_delete_subject,name='delete-subject'),
    # Admin parents
    path('approve-parents/<int:pk>', views.approve_parents_view,name='approve-parents'),
    path('admin-view-parents', views.admin_view_parents_view,name='admin-view-parents'),
    path('update-parents/<int:pk>', views.update_parents_view,name='update-parents'),
    path('delete-parents/<int:pk>', views.delete_parents_view,name='delete-parents'),
    path('admin-add-parents', views.admin_add_parents_view,name='admin-add-parents'),
    # Admin students
    path('admin-student', views.admin_student_view,name='admin-student'),
    path("approve-student/<int:pk>", views.approve_student_view, name="approve-student"),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    # Admin courses
    path('admin-course', views.admin_course_view,name='admin-course'),
    path('admin-add-course', views.admin_add_course_view,name='admin-add-course'),
    path('delete-course/<int:pk>', views.delete_course_view,name='delete-course'),
    path('admin-update-course/<int:pk>', views.admin_update_course_view,name='admin-update-course'),
    path('admin-view-course-detail/<int:pk>', views.admin_course_view_detail,name='admin-view-course-detail'),
    # Admin docs
    path('admin-blog', views.admin_blog_view,name='admin-blog'),
    path('admin-add-blog', views.admin_add_blog_view,name='admin-add-blog'),
    path('admin-view-blog', views.admin_view_blog_view,name='admin-view-blog'),
    path('delete-blog/<int:pk>', views.delete_blog_view,name='delete-blog'),
    path('admin-view-blog-detail/<int:pk>/', views.admin_view_blog_view_detail, name="admin-view-blog-detail"),
    path('update-blog/<int:pk>', views.updateblog,name='update-blog'),
    # Admin questions
    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),
    # Admin classroom
    path('admin-class', views.admin_view_class_view, name="admin-class"),
    path('admin-add-class', views.admin_add_class, name="admin-add-class"),
    path("admin-view-class/<slug>", views.admin_view_class_detail, name="admin-view-class"),
    path("admin-update-class/<slug>", views.admin_update_class, name="admin-update-class"),
    path('delete-class/<slug>', views.delete_class_view,name='delete-class'),
    path("admin-view-class-student/<slug>", views.admin_view_student_class, name="admin-view-class-student"),
    # Online room
    path('meeting/', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),

    # Static URL
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('user_attendance', views.quiz_attendance),
    # URL Face recognition
        path('about/', views.about),
    path('home/', views.home),
    path('attendance/', views.attendance),
    path('api/attendance/', views.AttendanceRecord.as_view()),
    path('sms',views.number),
    # Assignments 
    path('assignment/',views.assignments,name="assignment"),
    path('add_assign/',views.add_assign,name="add_assign"),
    path('sol_detail_t/<sol_id>', views.sol_detail_t, name='sol_detail_t'),
    path('view_assign/<assign_id>', views.view_assignments, name="view_assign"),
    # Quiz
    path('listofcourse/',views.view_listofcourse,name="listofcourse"),
    path('delete_listofcourse/<int:id>',views.delete_listofcourse,name="delete_listofcourse"),
    path('add_listofcourse/',views.add_listofcourse,name="add_listofcourse"),
    path('listofquiz/<int:id>',views.view_listofquiz,name="listofquiz"),
    path('add_listofquiz/',views.admin_add_listofquiz,name="add_listofquiz"),
    path('update_listofquiz/<int:id>',views.update_listofquiz, name="update_listofquiz"),
    path('update_listofcourse/<int:id>',views.update_listofcourse,name="update_listofcourse"),
    path('view_listofquiz/<int:id>',views.listofquiz_view_detail,name="view_listofquiz"),
    path('delete_listofquiz/<int:id>',views.delete_listofquiz,name="delete_listofquiz"),
    path('add_quiz',views.add_quiz,name="add_quiz"),
]