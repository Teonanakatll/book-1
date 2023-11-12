from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

from taggit.models import Tag

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # Инициализируем объект класса Paginator

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице
    # Извлекаем из запроса GET-параметр page, который указывает текущую страницу
    page = request.GET.get('page')
    try:
        # Получаем список объектов на нужной странице с помощью метода page() класса Paginator.
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})

# class PostListView(ListView):
#     # использовать переопределенный QuerySet модели вместо получения
#     # всех объектов. Вместо задания атрибута QuerySet мы могли бы указать
#     # модель model=Post, и тогда Django, используя стандартный менеджер мо-
#     # дели, получал бы объекты как Post.objects.all();
#     queryset = Post.published.all()
#     # использовать posts в качестве переменной контекста HTML-шаблона,
#     # в которой будет храниться список объектов. Если не указать атрибут context_
#     # object_name, по умолчанию используется переменная object_list;
#     context_object_name = 'posts'
#     paginate_by = 3
#     # использовать указанный шаблон для формирования страницы. Если бы
#     # мы не указали template_name, то базовый класс ListView использовал бы
#     # шаблон blog/post_list.html.
#     template_name = 'blog/post/list.html'
#
#     # Для поддержки постраничного вывода мы должны передавать объект стра-
#     # ницы, содержащий список статей, в HTML-шаблон. Базовый обработчик Django
#     # ListView передает этот объект в качестве переменной с именем page_obj, по-
#     # этому нужно немного откорректировать post/list.html и, подключая шаблон
#     # постраничного вывода, указать эту переменную:
#     # {% include "pagination.html" with page=page_obj %}


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # Список активных комментариев для этой статьи
    comments = post.comments.filter(active=True)
    new_comment = None

    # Если пользователь отправил коментарий
    if request.POST:
        # Передаём в форму донные введённые пользователем
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаём коментарий, но пока не сохраняем в базе данных commit=False. Метод save() создает объект модели,
            # с которой связана форма, и сохраняет его в базу данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем коментарий к текущей статье
            new_comment.post = post
            # Сохраняем комментарий в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()



    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})


def post_share(request, post_id):
    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    # Мы объявили переменную sent, она будет установлена в True после отправки сообщения. Будем использовать эту
    # переменную позже для отображения сообщения об успешной отправке в HTML-шаблоне.
    sent = False
    # Форма была отправленна на сохранение.
    if request.method == 'POST':
        # Заполненная форма отправляется методом POST (проверка заполненна ли форма).
        form = EmailPostForm(request.POST)
        # Если все поля формы прошли валидацию
        if form.is_valid():
            # cleaned_data - этот атрибут является словарём с полями формы и их значениями
            cd = form.cleaned_data
            # Отправка электронной почты

            # Так как нам нужно добавить в сообщение абсолютную ссылку на статью, мы используем метод объекта запроса
            # request.build_absolute_uri() и передаем в него результат выполнения get_absolute_url() статьи. Полученная
            # абсолютная ссылка будет содержать HTTP-схему и имя хоста.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f" {cd['name']} ({cd['email']}) recommends you reading '{post.title}'"
            message = f" Read '{post.title}' at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'bfaroon@yandex.ru', [cd['to']])
            sent = True
    else:
        # Если метод запроса – GET, необходимо отобразить пустую форму
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
              {'post': post, 'form': form, 'sent': sent})

