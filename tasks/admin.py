from django.contrib import admin
from .models import Task, Category, Priority, Note, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'priority', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('title', 'description')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'created_at')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_task', 'title', 'status')
    list_filter = ('status',)
    search_fields = ('title',)