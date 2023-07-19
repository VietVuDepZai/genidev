from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('studentclick', views.studentclick_view),
path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('studentsignup', views.student_signup_view,name='studentsignup'),
path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
path('student-exam', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),
path('view-exam/<int:pk>', views.student_view_exam_detail, name="view-exam"),
path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
path('student-view-blog', views.student_view_blog_view,name='student-view-blog'),
path('student-view-blog-detail/<int:pk>/', views.student_view_blog_view_detail, name="student-view-blog-detail"),
path('student-add-blog', views.student_add_blog_view,name='student-add-blog'),
path('delete-blog/<int:pk>', views.delete_blog_view,name='delete-blog'),
path('update-blog/<int:pk>', views.updatePost,name='update-blog'),
path('start_assign/<int:assignment_id>',views.submit, name="start_assign"),
path('assignment', views.assignments, name="assignment"),
path('solution/',views.sol_detail_t,name="solution"),
path('sol_detail_t/<sol_id>',views.detail_t,name="sol_detail_t"),
    path('listofcourse/',views.view_listofcourse,name="listofcourse"),
    path('listofquiz/<int:id>',views.view_listofquiz,name="listofquiz"),
path('view_listofquiz/<int:id>',views.listofquiz_view_detail,name="view_listofquiz"),
path('take_quiz/<int:pk>',views.take_quiz_view,name="take_quiz"),
path('start-quiz/<int:pk>', views.start_quiz_view,name='start-quiz'),
path('view-score',views.view_result_quiz,name="view-score"),
path('view-quiz/<int:pk>',views.check_marks_quiz,name="view-quiz"),
path("calculate-quiz",views.calculate_quiz_view,name="calculate-quiz"),
path('check-quiz/<int:pk>', views.check_marks_quiz,name='check-quiz'),

]