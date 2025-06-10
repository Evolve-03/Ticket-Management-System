from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/update/<int:project_id>/', views.update_project, name='update_project'),
    path('bugs/', views.bug_list, name='bug_list'),
    path('bugs/add/', views.add_bug, name='add_bug'),
    path('bugs/update/<int:bug_id>/', views.update_bug, name='update_bug'),
    path('bugs/remove/<int:bug_id>/', views.remove_bug, name='remove_bug'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/', views.user_list, name='user_list'),
    path('users/remove/<int:user_id>/', views.remove_user, name='remove_user'),
    path('bugs/export/', views.export_bugs, name='export_bugs'),
    path('bugs/import/', views.import_bugs, name='import_bugs'),

    # Login & Logout Views
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
