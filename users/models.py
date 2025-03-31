from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    job_role = models.CharField(max_length=100, blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True) # e.g., Entry, Mid, Senior
    streak = models.IntegerField(default=0) # Tracks consecutive days of activity

    def __str__(self):
        return self.username


class ActivityLog(models.Model):
    """
    Records the date a user performs a specific activity (e.g., answering a question).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    activity_date = models.DateField(default=timezone.now) # Store only the date

    class Meta:
        # Ensure a user has only one entry per date
        unique_together = ('user', 'activity_date')
        ordering = ['-activity_date'] # Order by date descending by default

    def __str__(self):
        return f"{self.user.username} - {self.activity_date.strftime('%Y-%m-%d')}"
