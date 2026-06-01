from django.db import models
from django.contrib.auth.models import User

class SymptomPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()  # Comma separated symptoms
    predicted_disease = models.CharField(max_length=255)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_disease}"
