from django.urls import include, path

from news.feeds import ArticleFeed
from news.views import ArticleDetailView, ArticleListView


urlpatterns = [
    path('feed/rss/', ArticleFeed(), name='news_article_feed'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='news_article_detail'),
    path('', ArticleListView.as_view(), name='news_article_list'),
]