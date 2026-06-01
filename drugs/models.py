from django.db import models

class DrugInfo(models.Model):
    name = models.CharField(max_length=255)
    usage = models.TextField()
    side_effects = models.TextField()
    dosage = models.CharField(max_length=255)

    def __str__(self):
        return self.name
