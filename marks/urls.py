from django.urls import path
from . import views

app_name = 'marks'

urlpatterns = [
    path('', views.marks_list, name='list'),
    path('upload/<int:course_id>/', views.upload_marks, name='upload'),
]