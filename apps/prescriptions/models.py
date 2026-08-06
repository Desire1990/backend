from django.db import models

class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='prescriptions/')
    notes = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rx {self.id} - {self.patient_name}"