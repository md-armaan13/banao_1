from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Appointment (models.Model) :
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.doctor.email + " " + str(self.start_date) + " " + str(self.start_time) + " " + str(self.end_time)  