from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_list, name='list_list'),
    path('list/add/', views.list_create, name='list_create'),
    path('list/<int:pk>/delete/', views.list_delete, name='list_delete'),
    path('list/<int:list_pk>/', views.task_list, name='task_list'),
    path('list/<int:list_pk>/toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
    path('list/<int:list_pk>/delete/<int:pk>/', views.delete_task, name='delete_task'),
]
