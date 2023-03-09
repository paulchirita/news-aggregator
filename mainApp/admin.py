from django.contrib import admin

from mainApp.models import Article, NewsWebsite, Topic

# Register your models here.
admin.site.register(NewsWebsite)
admin.site.register(Article)
admin.site.register(Topic)
