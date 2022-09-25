from django.urls import path
from todo import views

urlpatterns = [
    path('add-todo/', views.add_todo, name='add_todo'),
    path('get-todos/', views.get_todos, name='get_todos'),
    path('get-todo/<int:id>/', views.get_todo_by_id, name='get_todo_by_id'),
    path('update-todo/<int:id>/', views.update_todo, name='update_todo'),
    path('complete-todo/<int:id>/', views.complete_todo, name='complete_todo'),
    path('delete-todo/<int:id>/', views.delete_todo, name='delete_todo')
]