from django.urls import path

from . import views

app_name = 'tasktracker'
urlpatterns = [
    path('', views.signIn, name='signIn'),
    path('home/', views.home, name='home'),
    path('todoList/<str:list_id>/', views.todoList, name='todoList'),
    path('logout/', views.logout, name='logout'),
    path('signUp/', views.signUp, name='signUp'),
    path('signUp/postsignUp/', views.postsignUp),
    path('create_todoList/', views.create_todoList, name='create_todoList'),
    path('create_todoList/post_create_todoList/', views.post_create_todoList, name='post_create_todoList'),
    path('todoList/<str:list_id>/create_task/', views.create_task, name='create_task'),
    path('todoList/<str:list_id>/edit_task/<str:task_id>/', views.edit_task, name='edit_task'),
    path('todoList/<str:list_id>/edit_task/<str:task_id>/post_edit_task/', views.post_edit_task, name='post_edit_task'),
    path('todoList/<str:list_id>/share_list', views.share_list, name='share_list'),
    path('todoList/<str:list_id>/post_share_list', views.post_share_list, name='post_share_list'),
    path('todoList/<str:list_id>/delete_task/<str:task_id>/', views.delete_task, name='delete_task'),
    path('todoList/<str:list_id>/delete_list/', views.delete_list, name='delete_list'),
    path('todoList/<str:list_id>/search_task/', views.search_task, name='search_task'),
]
