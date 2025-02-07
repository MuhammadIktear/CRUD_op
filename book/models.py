from django.db import models

class Book(models.Model):
    image = models.URLField(max_length=200, blank=True, null=True)
    book_title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return f'Title: {self.book_title}'


