import datetime

from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
from django.forms import widgets


class Message(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tele = models.TextField(null=True, max_length=100)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.message


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class ChildCategory(models.Model):
    Category = models.ForeignKey(Category, related_name='ChildCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class CategoryHistory(models.Model):
    childcategory = models.ForeignKey(ChildCategory, related_name='ChildCategoryHistory', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.childcategory.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    childcategory = models.ForeignKey(ChildCategory, related_name='ArticleChildCategory', on_delete=models.CASCADE,
                                      max_length=50)
    info = models.TextField(null=True)
    options = models.TextField(null=True)
    conseil = models.TextField(null=True)
    complementes = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

    def images(self):
        return ArticleImage.objects.filter(article=self.id)


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name="articleimages", on_delete=models.CASCADE)
    name = models.FileField(upload_to='static/product_images')
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article.title


class Size1(models.Model):
    width = models.FloatField(null=True)
    height = models.FloatField(null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.width+'-'+self.height


class PaperType(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class PaperColor(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class FontColor(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class Side(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class Orientation(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class Finition(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class Specification(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='SpecificationArticle')
    customSize = models.BooleanField(null=True)
    size = models.ManyToManyField(Size1, related_name="SizeSpecification")
    paperType = models.ManyToManyField(PaperType, related_name="PaperSpecification")
    paperColor = models.ManyToManyField(PaperColor, related_name="PaperColorSpecification")
    fontColor = models.ManyToManyField(FontColor, related_name="FontColorSpecification")
    side = models.ManyToManyField(Side, related_name="SideSpecification")
    orientation = models.ManyToManyField(Orientation, related_name="OrientationSpecification")
    finition = models.ManyToManyField(Finition, related_name="FinitionSpecification")
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article.title


class Bestarticle(models.Model):
    article = models.OneToOneField(Article, related_name="bestarticle", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article.title


class Client(models.Model):
    user = models.OneToOneField(User, related_name="ClientUser", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, default='')
    civilite = models.CharField(max_length=10, default='')
    tele = models.TextField(max_length=14, default='')
    adresse1 = models.TextField(max_length=100, default='')
    adresse2 = models.TextField(max_length=150, default='')
    codepostal = models.TextField(max_length=150, default='')
    city = models.TextField(max_length=100, default='')
    country = models.TextField(max_length=100, default='')


class Search(models.Model):
    user = models.ForeignKey(User, related_name='search_user', on_delete=models.CASCADE, null=True, default='')
    title = models.TextField(null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
