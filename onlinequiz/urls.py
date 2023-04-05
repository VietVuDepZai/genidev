from django.urls import path,include,re_path
from django.contrib import admin
from quiz import views
from django.contrib.auth.views import LogoutView,LoginView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # Apps
    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path('parents/',include('parents.urls')),
    path('videocall/',include('videocall.urls')),
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
    # Admin parents
    path('admin-view-parents', views.admin_view_parents_view,name='admin-view-parents'),
    path('update-parents/<int:pk>', views.update_parents_view,name='update-parents'),
    path('delete-parents/<int:pk>', views.delete_parents_view,name='delete-parents'),
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
    # Admin docs
    path('admin-docs', views.admin_docs_view,name='admin-docs'),
    path('admin-add-docs', views.admin_add_docs_view,name='admin-add-docs'),
    path('admin-view-docs', views.admin_view_docs_view,name='admin-view-docs'),
    path('delete-docs/<int:pk>', views.delete_docs_view,name='delete-docs'),
    path('admin-view-docs-detail/<int:pk>/', views.admin_view_docs_view_detail, name="admin-view-docs-detail"),
    path('update-docs/<int:pk>', views.updateDocs,name='update-docs'),
    # Admin questions
    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),
    # Static URL
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]
