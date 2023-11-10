from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):
#     object_list = Post.published.all()
#     # Инициализируем объект класса Paginator
#     paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице
#     # Извлекаем из запроса GET-параметр page, который указывает текущую страницу
#     page = request.GET.get('page')
#     try:
#         # Получаем список объектов на нужной странице с помощью метода page() класса Paginator.
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # Если страница не является целым числом, возвращаем первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post/list.html', {'posts': posts})

class PostListView(ListView):
    # использовать переопределенный QuerySet модели вместо получения
    # всех объектов. Вместо задания атрибута QuerySet мы могли бы указать
    # модель model=Post, и тогда Django, используя стандартный менеджер мо-
    # дели, получал бы объекты как Post.objects.all();
    queryset = Post.published.all()
    # использовать posts в качестве переменной контекста HTML-шаблона,
    # в которой будет храниться список объектов. Если не указать атрибут context_
    # object_name, по умолчанию используется переменная object_list;
    context_object_name = 'posts'
    paginate_by = 3
    # использовать указанный шаблон для формирования страницы. Если бы
    # мы не указали template_name, то базовый класс ListView использовал бы
    # шаблон blog/post_list.html.
    template_name = 'blog/post/list.html'

    # Для поддержки постраничного вывода мы должны передавать объект стра-
    # ницы, содержащий список статей, в HTML-шаблон. Базовый обработчик Django
    # ListView передает этот объект в качестве переменной с именем page_obj, по-
    # этому нужно немного откорректировать post/list.html и, подключая шаблон
    # постраничного вывода, указать эту переменную:
    # {% include "pagination.html" with page=page_obj %}


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})