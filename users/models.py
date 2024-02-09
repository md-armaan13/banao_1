from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError



class Users (AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True)
    email = models.EmailField(unique=True)  

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
def validate_file_size(file) :
    max_size_mb = 10

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size should not exceed {max_size_mb} MB.')


class Profile (models.Model) :
    CATEGORY_PATIENT = 'patient'
    CATEGORY_DOCTOR = 'doctor'
    CATEGORY_CHOICES = [
        (CATEGORY_PATIENT, 'patient'),
        (CATEGORY_DOCTOR, 'doctor'),
    ]
    username = models.CharField(max_length=100 , null=False)
    firstName = models.CharField(max_length=100 , null=False)
    lastName = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users-images', blank=True, null=True ,validators=[validate_file_size])
    category = models.CharField(max_length=100 , choices=CATEGORY_CHOICES, default=CATEGORY_PATIENT)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100 ,null=False)
    city = models.CharField(max_length=100 , null=False)
    state = models.CharField(max_length=100 , null=False)
    pincode = models.CharField(max_length=100 ,null=False)
    
    def __str__(self) -> str:
        return self.firstName + " " + self.lastName
    