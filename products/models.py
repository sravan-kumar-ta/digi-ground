from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(upload_to='category', null=True)

    def __str__(self):
        return self.title
