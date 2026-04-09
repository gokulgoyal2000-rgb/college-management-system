from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fee_details, name='details'),
    path('add-payment/', views.add_payment, name='add_payment'),
]