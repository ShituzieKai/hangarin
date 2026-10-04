from django import forms
from django.forms import inlineformset_factory
from .models import Task, Category, Priority, Note, SubTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status']

SubTaskFormSet = inlineformset_factory(
    Task,
    SubTask,
    fk_name='parent_task',
    fields=['title', 'status'],
    extra=2,
    can_delete=False
)