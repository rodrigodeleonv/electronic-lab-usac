from django.urls import path  # , re_path
from web import views

app_name = 'web'

urlpatterns = [
    path('home/', views.home, name='home'),
]
