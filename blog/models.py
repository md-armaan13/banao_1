from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_size(file) :
    max_size_mb = 10

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size should not exceed {max_size_mb} MB.')


class Blog (models.Model):
    CATEGORY_MENTAL_HEALTH = 'Menatl Health'
    CATEGORY_HEART_DISEASE = 'Heart Disease'
    CATEGORY_COVID = 'Covid 19'
    CATEGORY_IMMUNIZATION = 'Immunization'
    CATEGORY_CHOICES = [
        (CATEGORY_MENTAL_HEALTH, 'Mental Health'),
        (CATEGORY_HEART_DISEASE, 'Heart Disease'),
        (CATEGORY_COVID, 'Covid 19'),
        (CATEGORY_IMMUNIZATION, 'Immunization'),
    ]
    title = models.CharField(null=False)
    summary = models.TextField(null=False)
    content = models.TextField(max_length=100)
    image = models.ImageField(
        upload_to='blog-images', blank=True, null=True, validators=[validate_file_size])
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default=CATEGORY_MENTAL_HEALTH)
    drafted = models.BooleanField(default=False)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
