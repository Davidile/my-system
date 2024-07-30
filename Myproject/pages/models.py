# models.py

from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    department_head = models.ForeignKey(User, on_delete=models.CASCADE, related_name='headed_department')

    def __str__(self):
        return self.name

class Task(models.Model):
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def calculate_score_percentage(self):
        total_tasks = Task.objects.filter(assigned_to=self.assigned_to, department=self.department).count()
        completed_tasks = Task.objects.filter(assigned_to=self.assigned_to, is_completed=True, department=self.department).count()

        if total_tasks == 0:
            return 0
        
        score_percentage = (completed_tasks / total_tasks) * 100
        return score_percentage

    calculate_score_percentage.short_description = 'Score (%)'

    def __str__(self):
        return self.description
