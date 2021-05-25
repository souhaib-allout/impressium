import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tele = models.TextField(null=True, max_length=100)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.message


class Article(models.Model):
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    info = models.TextField(null=True)
    options = models.TextField(null=True)
    conseil = models.TextField(null=True)
    complementes = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

class Search(models.Model):
    user_id=models.ForeignKey(User,related_name='search_user',on_delete=models.CASCADE)
    title=models.TextField(null=False)
    created_at=models.DateTimeField(default=datetime.datetime.now)

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name="articleimages", on_delete=models.CASCADE)
    name = models.FileField(upload_to='static/product_images')
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article.title


class Size(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='Sizearticle')
    width = models.FloatField()
    height = models.FloatField()
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article.title

    class Meta:
        ordering = ['price']


class Bestarticle(models.Model):
    article = models.ForeignKey(Article, related_name="bestarticle", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article.title


class Client(models.Model):
    user = models.OneToOneField(User, related_name="ClientUser", on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    civilite = models.CharField(max_length=10)
    tele = models.TextField(max_length=14)

# class models.User
