from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('register/', views.register, name='register'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('compose/', views.compose, name='compose'),
    path('email/<int:email_id>/', views.view_email, name='view_email'),
    path('contacts/', views.contacts, name='contacts'),
    path('profile/', views.profile, name='profile'),
]
