import django_filters as filters

from mainApp.models import Article


class ArticleFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="date", lookup_expr='lte')
    min_nr_likes = filters.NumberFilter(field_name="nrLikes", lookup_expr='gte')
    max_nr_likes = filters.NumberFilter(field_name="nrLikes", lookup_expr='lte')
    min_nr_saves = filters.NumberFilter(field_name="nrSaves", lookup_expr='gte')
    max_nr_saves = filters.NumberFilter(field_name="nrSaves", lookup_expr='lte')
    topic = filters.CharFilter(field_name="topic__name", lookup_expr="exact")
    news_website = filters.CharFilter(field_name="newsWebsite__name", lookup_expr="exact")

    class Meta:
        model = Article
        fields = ['title', 'newsWebsite__name', 'date', 'topic__name', 'nrLikes', 'nrSaves']