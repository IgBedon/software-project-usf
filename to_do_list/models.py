import os
from django.db import models
from django.contrib.auth.models import User

class Environment(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="collaborated_environments", blank=True)


    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField()
    color = models.CharField(max_length=25)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    title = models.CharField(max_length=100)  
    description = models.TextField()
    status = models.CharField(max_length=25)
    priority = models.IntegerField()
    deadline = models.DateField()
    categories = models.ManyToManyField(Category, related_name="tasks")
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    title = models.CharField(max_length=100, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='attachments/')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.title and self.file:
            self.title = os.path.splitext(self.file.name)[0]
        super().save(*args, **kwargs)