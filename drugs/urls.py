from django.urls import path
from . import views

app_name = 'drugs'

urlpatterns = [
    path('', views.search_view, name='search'),
]
