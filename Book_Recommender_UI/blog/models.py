from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Book(models.Model):
    ISBN = models.IntegerField()
    Title = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    YearofPublication = models.IntegerField()
    Publisher = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default='0')

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})