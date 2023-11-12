from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


# Django будет использовать название функции в качестве названия тега. Однако можно указать
# явно, как обращаться к тегу из шаблонов. Для этого достаточно передать в де-
# коратор аргумент name – @register.simple_tag(name='my_tag').
@register.simple_tag()
def total_posts():
    return Post.published.count()

# Инклюзивные теги должны возвращать только словари контекста, функция
# тега возвращает словарь переменных вместо простого значения.
# Чтобы задать любое другое
# количество статей, используйте такую запись: {% show_latest_posts 3 %.}.
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag()
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
