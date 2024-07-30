# admin.py

from django.contrib import admin
from .models import Task, Department

class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'assigned_to', 'department', 'calculate_score_percentage')
    readonly_fields = ('calculate_score_percentage','completion_date', )
    list_filter = ('department',  'is_completed', 'deadline')
    search_fields = ('description', 'assigned_to__username', 'assigned_to__email', 'department__name')

    def score(self, obj):
        return obj.calculate_score_percentage()
    score.short_description = 'Score (%)'

    def get_readonly_fields(self, request, obj=None):
        # Only make `is_completed` readonly for admins
        if request.user.is_superuser:
            return self.readonly_fields + ('is_completed',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # Only allow non-admins to update `is_completed`
        if not request.user.is_superuser:
            obj.is_completed = form.cleaned_data['is_completed']
        super().save_model(request, obj, form, change)

admin.site.register(Task, TaskAdmin)
admin.site.register(Department)
