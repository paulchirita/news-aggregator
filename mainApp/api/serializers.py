from rest_framework import serializers

from mainApp.models import Article, NewsWebsite, Topic, AppUser


class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ['email', 'first_name', 'last_name', 'savedArticles', 'preferredTopics', 'preferredNewsWebsites']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    # newsWebsite = serializers.HyperlinkedIdentityField(
    #     view_name='news_websites',
    #     lookup_field='name'
    # )
    # topic = serializers.HyperlinkedRelatedField(
    #     view_name='topics',
    #     lookup_field='name',
    #     # many=True,  # in case we decide an article can have more topics
    #     # read_only=True
    # )

    class Meta:
        model = Article
        # fields = "__all__"
        fields = ['title', 'newsWebsite', 'topic', 'articleText', 'date', 'nrLikes', 'nrSaves']


class NewsWebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsWebsite
        fields = ['name', 'url']


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']
