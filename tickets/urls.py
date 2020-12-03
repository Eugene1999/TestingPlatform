from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
]