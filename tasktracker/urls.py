from django.urls import path

from . import views

app_name = 'tasktracker'
urlpatterns = [
    path('', views.signIn, name='signIn'),
    path('home/', views.home),
    path('toDoList/', views.toDoList),
]