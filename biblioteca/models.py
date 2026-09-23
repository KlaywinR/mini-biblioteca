from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    year_of_publication = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title