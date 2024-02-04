from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('new_article/', ArticleCreateView.as_view(), name='create_article'),
    path('article_list/', ArticleListView.as_view(), name='article_list'),
    path('article_detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article_edit/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article_del/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
]