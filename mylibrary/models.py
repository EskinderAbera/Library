from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    pass

class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=84)
    description = models.TextField(null=True)
    publishDate = models.DateField(null= True)
    pageCount = models.IntegerField(null=True)
    createdAt = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = "images", blank = True, null = True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

    def created(self):
        return f"{self.createdAt.strftime('%b %d %Y')}"