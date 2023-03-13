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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from mainApp import views as mainapp_views
from rest_framework import routers, serializers, viewsets
from mainApp.models import Article, NewsWebsite, Topic


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'newsWebsite', 'topic', 'articleText', 'date', 'nrLikes', 'nrSaves', 'slug']


class NewsWebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsWebsite
        fields = ['name', 'url']


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class ArticleFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="date", lookup_expr='lte')
    min_nr_likes = filters.NumberFilter(field_name="nrLikes", lookup_expr='gte')
    max_nr_likes = filters.NumberFilter(field_name="nrLikes", lookup_expr='lte')
    min_nr_saves = filters.NumberFilter(field_name="nrSaves", lookup_expr='gte')
    max_nr_saves = filters.NumberFilter(field_name="nrSaves", lookup_expr='lte')

    class Meta:
        model = Article
        fields = ['title', 'newsWebsite__name', 'date', 'topic__name', 'nrLikes', 'nrSaves', 'slug']


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('title')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    order_fields = ['title', 'newsWebsite__name', 'date', 'topic__name', 'nrLikes', 'nrSaves', 'slug']
    search_fields = ['title', 'newsWebsite__name', 'date', 'topic__name', 'nrLikes', 'nrSaves', 'slug']


class NewsWebsiteViewSet(viewsets.ModelViewSet):
    queryset = NewsWebsite.objects.all().order_by('name')
    serializer_class = NewsWebsiteSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('name')
    serializer_class = TopicSerializer


router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'newsWebsites', NewsWebsiteViewSet)
router.register(r'topics', TopicViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("feed/", mainapp_views.Newsfeed.as_view(), name='feed'),
    path("", include("django.contrib.auth.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', mainapp_views.register, name='register'),
    path('api/', include(router.urls)),
    path('article/<slug:slug>/', mainapp_views.ArticleView.as_view(), name='article')
]
