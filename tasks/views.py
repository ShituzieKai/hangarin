from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, Category, Priority, Note, SubTask
from .forms import TaskForm, CategoryForm, PriorityForm, NoteForm, SubTaskFormSet

@login_required
def task_list(request):
    query = request.GET.get('q', '')
    user_tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = user_tasks.filter(title__icontains=query).prefetch_related('subtasks').order_by('-created_at')
    else:
        tasks = user_tasks.prefetch_related('subtasks').all().order_by('-created_at')

    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='Pending').count()
    completed_tasks = tasks.filter(status='Completed').count()

    context = {
        'tasks': tasks,
        'query': query,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        formset = SubTaskFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            subtasks = formset.save(commit=False)
            for subtask in subtasks:
                if subtask.title.strip():
                    subtask.parent_task = task
                    subtask.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        formset = SubTaskFormSet()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Add New Task'
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        formset = SubTaskFormSet(request.POST, instance=task)
        if form.is_valid() and formset.is_valid():
            form.save()
            subtasks = formset.save(commit=False)
            for subtask in subtasks:
                if subtask.title.strip():
                    subtask.parent_task = task
                    subtask.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        formset = SubTaskFormSet(instance=task)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Edit Task'
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def category_list(request):
    if hasattr(Category, 'user'):
        categories = Category.objects.filter(user=request.user)
    else:
        categories = Category.objects.all()
    return render(request, 'tasks/category_list.html', {'categories': categories})

@login_required
def priority_list(request):
    # Filter by user if Priority model has a Foreign Key to User
    if hasattr(Priority, 'user'):
        priorities = Priority.objects.filter(user=request.user)
    else:
        priorities = Priority.objects.all()
    return render(request, 'tasks/priority_list.html', {'priorities': priorities})

@login_required
def note_list(request):
    if hasattr(Note, 'user'):
        notes = Note.objects.filter(user=request.user)
    else:
        notes = Note.objects.all()
    return render(request, 'tasks/note_list.html', {'notes': notes})

@login_required
def add_subtask(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        title = request.POST.get('subtask_title', '').strip()
        if title:
            SubTask.objects.create(
                parent_task=task,
                title=title,
                status='Pending'
            )
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))

@login_required
def toggle_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id, parent_task__user=request.user)
    subtask.status = 'Pending' if subtask.status == 'Completed' else 'Completed'
    subtask.save()
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))

@login_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id, parent_task__user=request.user)
    subtask.delete()
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))