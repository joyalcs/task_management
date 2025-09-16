from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import CustomUser, Task
from .forms import TaskForm, UserForm, AdminForm


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user and user.role in ['admin', 'superadmin']:
            login(request, user)
            return redirect('task:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions')
    
    return render(request, 'admin/login.html')

def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')

@login_required
def admin_dashboard_view(request):
    if request.user.role not in ['admin', 'superadmin']:
        return HttpResponseForbidden("Access denied")
    
    context = {}
    print(request.user.role)
    if request.user.role == 'superadmin':
        context.update({
            'total_users': CustomUser.objects.filter(role='user').count(),
            'total_admins': CustomUser.objects.filter(role='admin').count(),
            'total_tasks': Task.objects.count(),
            'completed_tasks': Task.objects.filter(status='completed').count(),
        })
    else: 
        assigned_users = CustomUser.objects.filter(assigned_admin=request.user)
        context.update({
            'assigned_users': assigned_users.count(),
            'total_tasks': Task.objects.filter(assigned_to__in=assigned_users).count(),
            'completed_tasks': Task.objects.filter(
                assigned_to__in=assigned_users, 
                status='completed'
            ).count(),
        })
    
    return render(request, 'admin/dashboard.html', context)

@login_required
def user_management_view(request):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access denied")
    
    users = CustomUser.objects.filter(role='user')
    return render(request, 'admin/user_management.html', {'users': users})

@login_required
def admin_management_view(request):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access denied")
    
    admins = CustomUser.objects.filter(role='admin')
    return render(request, 'admin/admin_management.html', {'admins': admins})

@login_required
def task_management_view(request):
    if request.user.role not in ['admin', 'superadmin']:
        return HttpResponseForbidden("Access denied")
    
    if request.user.role == 'superadmin':
        tasks = Task.objects.all()
    else:  # admin
        assigned_users = CustomUser.objects.filter(assigned_admin=request.user)
        tasks = Task.objects.filter(assigned_to__in=assigned_users)
    
    return render(request, 'admin/task_management.html', {'tasks': tasks})

@login_required
def create_user_view(request):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access denied")
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('task:user_management')
    else:
        form = UserForm()
    
    return render(request, 'admin/create_user.html', {'form': form})


@login_required
def create_admin_view(request):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access denied")
    
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin created successfully')
            return redirect('task:admin_management')
    else:
        form = AdminForm()
    
    return render(request, 'admin/create_admin.html', {'form': form})



@login_required
def create_task_view(request):
    if request.user.role not in ['admin', 'superadmin']:
        return HttpResponseForbidden("Access denied")
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully')
            return redirect('task:task_management')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'admin/create_task.html', {'form': form})

@login_required
def task_reports_view(request):
    if request.user.role not in ['admin', 'superadmin']:
        return HttpResponseForbidden("Access denied")
    
    if request.user.role == 'superadmin':
        completed_tasks = Task.objects.filter(status='completed')
    else:  # admin
        assigned_users = CustomUser.objects.filter(assigned_admin=request.user)
        completed_tasks = Task.objects.filter(
            assigned_to__in=assigned_users, 
            status='completed'
        )
    
    return render(request, 'admin/task_reports.html', {'tasks': completed_tasks})

@login_required
def delete_user_view(request, user_id):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access denied")
    
    user = get_object_or_404(CustomUser, id=user_id, role='user')
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('task:user_management')

@login_required
def delete_admin_view(request, admin_id):
    if request.user.role != 'superadmin':
        return HttpResponseForbidden("Access denied")
    
    admin = get_object_or_404(CustomUser, id=admin_id, role='admin')
    admin.delete()
    messages.success(request, 'Admin deleted successfully')
    return redirect('task:admin_management')

@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('task:admin_login')