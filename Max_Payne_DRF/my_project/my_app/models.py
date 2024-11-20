from django.db import models

class Parent(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    age=models.IntegerField(default=1)

# Create your models here.
class Children(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    age=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey(Parent,on_delete=models.CASCADE)
    