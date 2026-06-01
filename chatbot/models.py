from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Chat Histories"

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
