from django.db import models
from django.conf import settings
from django.utils import timezone

class QuizAttempt(models.Model):
    """
    Stores the results of a single quiz attempt by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    questions_attempted = models.PositiveIntegerField()
    questions_correct = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp'] # Show most recent attempts first

    def __str__(self):
        return f"{self.user.username} - {self.questions_correct}/{self.questions_attempted} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def score_percentage(self):
        """
        Calculates the score percentage for the attempt.
        """
        if self.questions_attempted > 0:
            return round((self.questions_correct / self.questions_attempted) * 100, 2)
        return 0.0
