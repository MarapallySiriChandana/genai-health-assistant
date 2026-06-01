from django.urls import path
from . import views

app_name = 'ml_module'

urlpatterns = [
    path('', views.checker_view, name='checker'),
]
