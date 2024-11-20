from django.db import models

# Create your models here.
class Authors(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    date_of_birth=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

class Books(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    authors=models.ManyToManyField(Authors)

    def __str__(self):
        return self.title 

