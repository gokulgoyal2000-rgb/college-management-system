from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.library_view, name='view'),
    path('issue/', views.issue_book, name='issue'),
    path('return/<int:issue_id>/', views.return_book, name='return'),
]