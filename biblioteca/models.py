from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)
    link = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        return self.title
