"""newsaggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainApp import views
from rest_framework import routers, serializers, viewsets
from mainApp.models import Article, NewsWebsite, Topic


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'newsWebsite', 'topic', 'articleText', 'date', 'nrLikes', 'nrSaves']


class NewsWebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsWebsite
        fields = ['name', 'url']


class NewsWebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('title')
    serializer_class = ArticleSerializer


class NewsWebsiteViewSet(viewsets.ModelViewSet):
    queryset = NewsWebsite.objects.all().order_by('name')
    serializer_class = NewsWebsiteSerializer


class TopicWebsiteViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('name')
    serializer_class = NewsWebsiteSerializer


router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'newsWebsites', NewsWebsiteViewSet)
router.register(r'topics', TopicWebsiteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index.as_view(), name='index'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
