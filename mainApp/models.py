from django.db import models


# Create your models here.


class NewsWebsite(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=500)


class Topic(models.Model):
    name = models.CharField


class Article(models.Model):
    title = models.CharField(max_length=200)
    newsWebsite = models.ForeignKey(NewsWebsite, on_delete=models.CASCADE)
    articleText = models.TextField
    date = models.DateTimeField
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    nrLikes = models.IntegerField
    nrSaves = models.IntegerField


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    savedArticles = models.ManyToManyField(Article)
    preferredTopics = models.ManyToManyField(Topic)
    preferredNewsWebsites = models.ManyToManyField(NewsWebsite)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    time = models.DateTimeField
    text = models.TextField
    repliedTo = models.ForeignKey('self', on_delete=models.CASCADE)
