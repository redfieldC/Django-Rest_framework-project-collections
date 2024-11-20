from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

mobile_number_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Mobile number must be exactly 10 digits and contain only numbers"
)

class CustomUser(AbstractUser):
    mobile_number = models.CharField(
        max_length=10, unique=True, validators=[mobile_number_validator]
    )

class Task(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_completed=models.BooleanField(default=False)