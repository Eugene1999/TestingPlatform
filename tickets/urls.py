from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ticket-detail/<int:pk>/', views.ticket_detail, name='ticket-detail'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('pass-test/<int:pk>/', views.pass_test, name='pass-test'),
]