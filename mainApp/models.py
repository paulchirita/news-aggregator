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
    date = models.DateTimeField(blank=True, null=True)
    # todo: can't an article have more topics? so many to many relationship?
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="articles")
    nrLikes = models.IntegerField()
    nrSaves = models.IntegerField()
    slug = models.SlugField(max_length=200, unique=True)
    nrLikes = models.PositiveIntegerField(default=0)
    nrSaves = models.PositiveIntegerField(default=0)

    def saved_by_user(self, user_pk):
        return self.saved_by_set.get(pk=user_pk).exists()

    def update_nr_saves(self, count):
        self.nrSaves += count

    def update_nr_likes(self, count):
        self.nrLikes += count


class AppUser(AbstractUser, models.Model):
    savedArticles = models.ManyToManyField(Article, related_name="saved_by")
    preferredTopics = models.ManyToManyField(Topic, related_name="preferred_by")
    preferredNewsWebsites = models.ManyToManyField(NewsWebsite, related_name="preferred_by")
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ["id"]
        db_table = "users"

    def get_preferred_topics(self):
        return self.preferredTopics.all() if self.preferredTopics.all() else Topic.objects.all()

    def get_preferred_news_websites(self):
        return self.preferredNewsWebsites.all() if self.preferredNewsWebsites.all() else NewsWebsite.objects.all()


class Comment(models.Model):
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="comments")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField()
    text = models.TextField()
    repliedTo = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies")
