from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Bug, Project
from .forms import BugForm, ProjectForm, BugUpdateForm
from .forms import CustomUserCreationForm
from django.contrib import messages


@login_required
def home(request):
    if request.user.is_superuser:
        user_bugs = Bug.objects.all()
    else:
        user_bugs = Bug.objects.filter(assigned_to=request.user)

    return render(request, 'tracker/home.html', {'bugs': user_bugs})


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/projects.html', {'projects': projects})

@login_required
def add_project(request):
    if not request.user.is_superuser:
        return redirect('project_list')

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'tracker/add_project.html', {'form': form})

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'tracker/update_project.html', {'form': form})

@login_required
def bug_list(request):
    bugs = Bug.objects.all()
    return render(request, 'tracker/bugs.html', {'bugs': bugs})

@login_required
def add_bug(request):
    if request.method == "POST":
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.created_by = request.user
            bug.modified_by = request.user
            bug.save()
            return redirect('bug_list')
    else:
        form = BugForm()
    
    return render(request, 'tracker/add_bug.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'tracker/users.html', {'users': users})

@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect('user_list')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('user_list')
        else:
            messages.error(request, "Error creating user. Please check the form.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'tracker/add_user.html', {'form': form})

@login_required
def remove_user(request, user_id):
    if request.user.is_superuser:
        User.objects.get(id=user_id).delete()
    return redirect('user_list')

@login_required
def update_bug(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)

    if request.method == 'POST':
        form = BugUpdateForm(request.POST, instance=bug)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.modified_by = request.user
            bug.save()
            messages.success(request, f"Bug '{bug.title}' updated successfully!")
            return redirect('bug_list')  # Redirect to the bug list or details page
        else:
            messages.error(request, "Error updating bug. Please check the form.")
    else:
        form = BugUpdateForm(instance=bug)

    return render(request, 'tracker/update_bug.html', {'form': form, 'bug': bug})