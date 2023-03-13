from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from mainApp.api import permissions
from mainApp.api.filters import ArticleFilter
from mainApp.models import Article, NewsWebsite, Topic, AppUser
from mainApp.api.serializers import ArticleSerializer, NewsWebsiteSerializer, TopicSerializer, AppUserSerializer


class AppUserViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = AppUserSerializer
    queryset = AppUser.objects.all()
    permission_classes = [permissions.IsOwner]  # users can only edit & read their own attributes

    @action(detail=True, methods=['post'])
    def update_preferred_topics(self, request, pk):
        topic_ids = request.data.get('topics')
        valid = []
        for topic_id in topic_ids:
            try:
                topic = Topic.objects.get(pk=topic_id)
                valid.append(topic)
            except Topic.DoesNotExist:
                pass
        if valid:
            request.user.preferredTopics.set(valid)
        # return Response({"user": AppUser.objects.get(pk=pk), "message": "Updated preferred topics"}, template_name="",
        #                 status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_preferred_website(self, request, pk):
        website_ids = request.data.get('websites')
        invalid, valid = [], []
        for website_id in website_ids:
            try:
                website = NewsWebsite.objects.get(pk=website_id)
                valid.append(website)
            except NewsWebsite.DoesNotExist:
                invalid.append(website_id)
        if valid:
            request.user.preferredNewsWebsites.set(valid)
        # return Response({"user": AppUser.objects.get(pk=pk), "message": "Updated preferred topics"}, template_name="",
        #                 status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def save_article(self, request, pk):
        article_ids = request.data.get('articles')
        invalid = []
        for article_id in article_ids:
            try:
                article = Article.objects.get(pk=article_id)
                request.user.savedArticles.add(article)
            except Article.DoesNotExist:
                invalid.append(article_id)
        # return Response({"user": AppUser.objects.get(pk=pk), "message": "Updated preferred topics"}, template_name="",
        #                 status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_saved_article(self, request, pk):
        article = Article.objects.filter(pk=request.data.get("article_pk"))
        if article.exists():
            request.user.savedArticles.delete(article)
        # return Response({"user": AppUser.objects.get(pk=pk), "message": "Updated preferred topics"}, template_name="",
        #                 status=status.HTTP_200_OK)


class ArticleViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    View class for the Article model with list and retrieve endpoints. Users can only request a set of articles or
     an individual article.
    """
    queryset = Article.objects.all().order_by('title')  # todo: not by date?
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    order_fields = ['title', 'newsWebsite__name', 'date', 'topic__name', 'nrLikes', 'nrSaves']
    search_fields = ['title', 'newsWebsite__name', 'date', 'topic__name', 'nrLikes', 'nrSaves']

    def get_queryset(self):
        if not self.request.user.is_authenticated or self.request.user.is_superuser:
            return Article.objects.all().order_by('title')
        topics_subset = self.request.user.get_preferred_topics()
        news_websites_subset = self.request.user.get_preferred_news_websites()
        return Article.objects.filter(newsWebsite__in=news_websites_subset, topic__in=topics_subset).order_by('title')

    # fixme: AttributeError at /api/articles/
    #  Got AttributeError when attempting to get a value for field `title` on serializer `ArticleSerializer`.
    #  The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
    #  Original exception text was: 'QuerySet' object has no attribute 'title'.
    # def list(self, request, *args, **kwargs):
    #     objects = self.get_queryset()
    #     if request.accepted_renderer.format == 'html':
    #         # TemplateHTMLRenderer takes a context dict,
    #         # and additionally requires a 'template_name'.
    #         # It does not require serialization.
    #         data = {'articles': objects}
    #         return Response(data, template_name='feed.html')
    #     # JSONRenderer requires serialized data as normal.
    #     return Response(ArticleSerializer(instance=objects, context={'request': request}).data)

    @action(detail=False, methods=['get'])
    def articles_by_topic(self, request, pk):
        article = Article.objects.filter(pk=pk)
        if article.exists():
            request.user.savedArticles.add(article)
            return article
        return Article.objects.all()
        # return Response({"user": AppUser.objects.get(pk=pk), "message": "Updated preferred topics"}, template_name="",
        #                 status=status.HTTP_200_OK)


class NewsWebsiteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = NewsWebsite.objects.all().order_by('name')
    serializer_class = NewsWebsiteSerializer


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Topic.objects.all().order_by('name')
    serializer_class = TopicSerializer