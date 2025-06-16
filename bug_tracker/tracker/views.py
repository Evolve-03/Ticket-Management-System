import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Bug, Project
from .forms import BugForm, ProjectForm, BugUpdateForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator


@login_required
def home(request):
    bugs_queryset = Bug.objects.filter(assigned_to=request.user).order_by('-created_at')
    paginator = Paginator(bugs_queryset, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/home.html', {'page_obj': page_obj})
    


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
    bug_queryset = Bug.objects.all().order_by('-created_at')
    paginator = Paginator(bug_queryset, 6)  # 6 bugs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/bugs.html', {'page_obj': page_obj})     

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
def remove_bug(request, bug_id):
    Bug.objects.get(id=bug_id).delete()
    return redirect('bug_list')

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


@login_required
def export_bugs(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ticket ID', 'Changeset', 'Title', 'Description', 'Status', 'Project', 'Assigned To'])

    for bug in Bug.objects.all():
        writer.writerow([
            bug.ticket_number,
            bug.changeset_id,
            bug.title,
            bug.description,
            bug.status,
            bug.project.name if bug.project else '',
            bug.assigned_to.username if bug.assigned_to else ''
        ])

    return response

@login_required
def import_bugs(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            project_name = row['Project'].strip()
            username = row['Assigned To'].strip()

            # Get or create project
            project, created_project = Project.objects.get_or_create(name=project_name)
            if created_project:
                messages.info(request, f"Project '{project_name}' was created.")

            # Get or create user
            assigned_to = User.objects.filter(username=username).first()
            if not assigned_to:
                assigned_to = User.objects.create_user(username=username, password='tickets@123')
                messages.info(request, f"User '{username}' was created with default password.")

            # Create the bug
            Bug.objects.create(
                changeset_id=row['Changeset id'].strip(),
                title=row['Title'].strip(),
                description=row['Description'].strip(),
                status=row['Status'].strip(),
                project=project,
                assigned_to=assigned_to
            )

        messages.success(request, "Bug data imported successfully.")
        return redirect('bug_list')

    return render(request, 'tracker/import_bugs.html')