from django.contrib.auth.models import AbstractUser
from django.db import models


class NewsWebsite(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=500)


class Topic(models.Model):
    name = models.CharField(max_length=100, default="Test topic")


class Article(models.Model):
    title = models.CharField(max_length=200)
    newsWebsite = models.ForeignKey(NewsWebsite, on_delete=models.CASCADE, related_name="articles")
    articleText = models.TextField()
    date = models.DateTimeField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="articles")
    nrLikes = models.IntegerField()
    nrSaves = models.IntegerField()
    slug = models.SlugField(max_length=200, unique=True)

class AppUser(AbstractUser, models.Model):
    savedArticles = models.ManyToManyField(Article)
    preferredTopics = models.ManyToManyField(Topic)
    preferredNewsWebsites = models.ManyToManyField(NewsWebsite)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ["id"]
        db_table = "users"


class Comment(models.Model):
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="comments")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField()
    text = models.TextField()
    repliedTo = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies")
