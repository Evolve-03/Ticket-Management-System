from django.contrib.auth.models import User
from django.db import models
from django.db import connection

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Bug(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Ready for Testing', 'Ready for Testing'),
        ('Reopened', 'Reopened'),
        ('Moved to UAT', 'Moved to UAT'),
        ('Moved to Production', 'Moved to Production'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_to')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_by')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=20, unique=True, editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Get the max id ever used, including deleted records
            with connection.cursor() as cursor:
                cursor.execute("SELECT seq FROM sqlite_sequence WHERE name=%s", [self._meta.db_table])
                row = cursor.fetchone()
                next_id = (row[0] + 1) if row else 1
            project_code = self.project.name[:3].upper() if self.project and self.project.name else "PRJ"
            self.ticket_number = f"{project_code}-{next_id:05d}"
        super().save(*args, **kwargs)
        
    changeset_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
