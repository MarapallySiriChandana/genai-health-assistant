from django.urls import path
from . import views

app_name = 'image_module'

urlpatterns = [
    path('', views.upload_view, name='upload'),
]
