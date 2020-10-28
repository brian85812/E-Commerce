from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)

    def get_category_url(self):
        return reverse("main:index_by_category", kwargs={
            'category_id': self.id
        })

    def __str__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="image")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:product", kwargs={
            'pk': self.id

        })
