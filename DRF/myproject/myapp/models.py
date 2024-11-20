from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    description = models.TextField()         # Description of the category

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price field
    created_at = models.DateTimeField(default=timezone.now)  # Date created
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)  # ForeignKey field

    def __str__(self):
        return self.name
