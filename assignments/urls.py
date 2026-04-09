from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.assignment_list, name='list'),
    path('create/', views.create_assignment, name='create'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit'),
    path('grade/<int:assignment_id>/', views.grade_submissions, name='grade'),
]