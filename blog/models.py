from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Model for Post Table


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    # Tells django that if a user is deleted, their posts should be
    # deleted as well
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# Create your models here.

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
