from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('in_work', views.in_work, name='in_work'),
    path('completed', views.completed_task, name='completed'),
    path('remaining', views.remaining, name='remaining'),
    path('add_task', views.add_task, name='add_task'),
    path('delete/<str:task_id>', views.delete_task, name='delete'),
    path('detail/<str:task_id>', views.task_detail, name='task_detail'),
    path('toggle_complete/<str:task_id>', views.toggle_complete, name='toggle_complete'),
    path('remove_task/<str:task_id>', views.remove_task, name='remove_task'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
]
