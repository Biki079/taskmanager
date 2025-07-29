from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

def logout_view(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task-list')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'tasks/tasks_form.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(complete=True).count()
    incomplete_tasks = tasks.filter(complete=False).count()

    context = {
        'user': user,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
    }
    return render(request, 'tasks/profile.html', context)
