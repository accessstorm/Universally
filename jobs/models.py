from django.db import models
from .utils import extract_skills_from_description

class Job(models.Model):
    """
    Represents a job posting.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    key_skills = models.TextField(blank=True, help_text="Comma-separated list of extracted skills")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Extract skills from description before saving
        self.key_skills = extract_skills_from_description(self.description)
        super().save(*args, **kwargs) # Call the "real" save() method.

    def __str__(self):
        return self.title
