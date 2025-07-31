
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

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
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})
# Custom login view to redirect to dashboard after login
from django import forms
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})


@login_required
def task_list(request):
    if request.method == 'POST':
        # Quick add task
        if request.POST.get('quick_add'):
            title = request.POST.get('quick_title', '').strip()
            description = request.POST.get('quick_description', '').strip()
            if title:
                Task.objects.create(user=request.user, title=title, description=description)
        else:
            task_id = request.POST.get('task_id')
            complete = request.POST.get('complete') == '1'
            try:
                task = Task.objects.get(pk=task_id, user=request.user)
                task.complete = complete
                task.save()
            except Task.DoesNotExist:
                pass
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(complete=True).count()
    percent = int((completed / total) * 100) if total > 0 else 0
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'percent': percent,
    })


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
    # Get or create user profile
    from .models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=user)

    context = {
        'user': user,
        'profile': profile,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
    }
    return render(request, 'tasks/profile.html', context)

@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('profile')
    return render(request, 'tasks/delete_task_confirm.html', {'task': task})

@login_required
def get_all_tasks(request):
    tasks = Task.objects.all().select_related('user').order_by('-created')
    return render(request, 'tasks/get_all_task.html', {'tasks': tasks})

def dashboard(request):
    user = request.user
    # Recent tasks (last 5 created)
    tasks = Task.objects.filter(user=user).order_by('-created')[:5]
    # All updates (recently updated or completed tasks, last 10)
    updates = Task.objects.filter(user=user).order_by('-updated')[:10]
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(user=user, complete=True).count()
    incomplete_tasks = Task.objects.filter(user=user, complete=False).count()

    # For circular progress bar
    percent_complete = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    # SVG circle: circumference = 2 * pi * r, r=54
    circumference = 2 * 3.1416 * 54
    stroke_offset = circumference - (percent_complete / 100) * circumference

    context = {
        'user': user,
        'tasks': tasks,
        'updates': updates,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
        'percent_complete': percent_complete,
        'stroke_offset': stroke_offset,
        'circumference': circumference,
    }
    return render(request, 'tasks/dashboard.html', context)