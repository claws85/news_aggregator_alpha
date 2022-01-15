
from django.db import models
from django.db.models.fields import DateField, URLField


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    url = URLField(unique=True)
    source = models.CharField(max_length=200)
    date = DateField(auto_now_add=True)
    keywords = models.CharField(max_length=200)

    class Meta:
        get_latest_by = 'date'