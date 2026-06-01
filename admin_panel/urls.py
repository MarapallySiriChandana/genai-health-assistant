from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('chats/', views.chat_logs, name='chat_logs'),
    path('predictions/', views.predictions, name='predictions'),
    path('images/', views.image_analyses, name='image_analyses'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
