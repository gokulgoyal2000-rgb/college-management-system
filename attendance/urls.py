from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='list'),
    path('mark/<int:course_id>/', views.mark_attendance, name='mark'),
]