from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    
    path('categories/', views.category_list, name='category_list'),
    path('priorities/', views.priority_list, name='priority_list'),
    path('notes/', views.note_list, name='note_list'),

    path('task/<int:task_id>/add-subtask/', views.add_subtask, name='add_subtask'),
    path('subtask/<int:subtask_id>/toggle/', views.toggle_subtask, name='toggle_subtask'),
    path('subtask/<int:subtask_id>/delete/', views.delete_subtask, name='delete_subtask'),
]