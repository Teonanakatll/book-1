from django.urls import path
from . import views

# RSS
from .feeds import LatestPostFeed


# Пространство имён приложения
app_name = 'blog'

urlpatterns = [
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    path('search/', views.post_search, name='post_search'),

    # RSS
    path('feed/', LatestPostFeed(), name='post_feed'),

    # url - для фильтрации статей по тегу
    # Мы используем преобразователь slug, для того чтобы ограничить воз-можные символы URL’а в качестве тега
    # (могут быть использованы только прописные буквы, числа, нижние подчеркивания и дефисы).
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
