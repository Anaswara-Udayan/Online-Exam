from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:exam_id>/details/', views.exam_details, name='exam_details'),
    path('exams/<int:exam_id>/start/', views.start_exam, name='start_exam'),
    path('exams/<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),
    path('exams/<int:exam_id>/results/', views.exam_results, name='exam_results'),
    path('marks/', views.available_exams, name='available_exams'),
    path('marks/<int:exam_id>/', views.view_marks, name='view_marks'),
    path('about/', views.about, name='about'),
    path('help/', views.help_center_view, name='help_center'),
    path('logout/', views.logout_view, name='logout'),

]