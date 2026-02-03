

from django.db import models

class EquipmentDataset(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"

