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

    # Profile customization fields
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.png')
    bio = models.CharField(max_length=150, blank=True, help_text="A short bio about yourself.")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags (e.g., Python, Django, Learner)")
    about = models.TextField(blank=True, help_text="More details about you, your skills, or interests.")
    website_link = models.URLField(max_length=200, blank=True)
    github_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.username

    # Method to get profile image URL (handles default)
    @property
    def get_profile_image_url(self):
        try:
            url = self.profile_image.url
        except (ValueError, AttributeError):
            # Handle cases where image is not set or file is missing
            # Point to a default image in your static files
            from django.templatetags.static import static
            url = static('images/default_profile.png') # Adjust path as needed
        return url


# Removed ActivityLog model definition
