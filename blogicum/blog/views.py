from django.shortcuts import render
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm, CommentEditForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Count
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.forms import UserChangeForm


def index(request):
    """Главная страница со списком постов"""
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Лента записей',
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    """Страница отдельного поста"""
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        id=id
    )

    is_author = request.user == post.author
    is_published = (
        post.is_published
        and post.pub_date <= timezone.now()
        and post.category.is_published
    )

    if not is_published and not is_author:
        raise Http404("Пост не найден")

    if is_author:
        comments = post.comments.select_related('author')
    else:
        comments = post.comments.filter(
            is_published=True
        ).select_related('author')

    comment_form = CommentForm()

    context = {
        'title': post.title,
        'post': post,
        'comments': comments,
        'form': comment_form,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'Категория: {category.title}',
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def user_posts(request, username):
    user = get_object_or_404(User, username=username)

    if request.user == user:
        posts = Post.objects.filter(author=user).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    else:
        posts = Post.objects.filter(
            author=user,
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user,
        'page_obj': page_obj,
        'title': f'Страница пользователя {user.username}',
    }
    return render(request, 'blog/profile.html', context)


@login_required
def post_create(request):
    """Создание новой публикации"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_published = True
            post.save()

            send_post_created_email(request.user, post)

            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm(author=request.user)

    context = {
        'form': form,
        'title': 'Добавить новую публикацию'
    }
    return render(request, 'blog/create.html', context)


def send_post_created_email(user, post):
    """Отправка письма о создании поста"""
    subject = f'Ваш пост "{post.title}" опубликован!'
    message = f'''
    Здравствуйте, {user.username}!

    Ваш пост "{post.title}" успешно опубликован на Blogicum.

    Вы можете просмотреть его по ссылке:
    http://127.0.0.1:8000/posts/{post.id}/

    С уважением,
    Команда Blogicum
    '''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


@login_required
def post_edit(request, id):
    """Редактирование существующей публикации"""
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return redirect('blog:post_detail', id=id)

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
            author=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = PostForm(instance=post, author=request.user)

    context = {
        'form': form,
        'title': 'Редактирование публикации'
    }
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, id):
    """Добавление комментария к публикации"""
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = CommentForm()

    return post_detail(request, id)


@login_required
def edit_comment(request, id, comment_id):
    """Редактирование комментария"""
    comment = get_object_or_404(Comment, id=comment_id, post_id=id)

    if comment.author != request.user:
        return HttpResponseForbidden(
            "У вас нет прав для редактирования этого комментария"
        )

    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = CommentEditForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
        'post': comment.post,
        'title': 'Редактирование комментария'
    }
    return render(request, 'blog/comment.html', context)


@login_required
def post_delete(request, id):
    """Удаление публикации (подтверждение + удаление)"""
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return redirect('blog:post_detail', id=id)

    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(
            request,
            f'Публикация "{post_title}" успешно удалена.'
        )
        return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
            'title': 'Удаление публикации',
            'delete_mode': True
        }
        return render(request, 'blog/create.html', context)


@login_required
@require_POST
def post_delete_confirm(request, id):
    """Фактическое удаление публикации"""
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return HttpResponseForbidden(
            "У вас нет прав для удаления этой публикации"
        )

    post_title = post.title
    post.delete()

    messages.success(request, f'Публикация "{post_title}" успешно удалена.')
    return redirect('blog:profile', username=request.user.username)


@login_required
def delete_comment(request, id, comment_id):
    """Удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id, post_id=id)

    if comment.author != request.user:
        return redirect('blog:post_detail', id=id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=id)
    else:
        context = {
            'comment': comment,
            'post': comment.post,
            'title': 'Удаление комментария'
        }
        return render(request, 'blog/comment.html', context)


@login_required
@require_POST
def delete_comment_confirm(request, id, comment_id):
    """Фактическое удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id, post_id=id)

    if comment.author != request.user:
        return HttpResponseForbidden(
            "У вас нет прав для удаления этого комментария"
        )

    comment.delete()
    return redirect('blog:post_detail', id=id)


def send_welcome_email(user):
    """Отправка приветственного письма новому пользователю"""
    subject = 'Добро пожаловать в Blogicum!'
    message = f'''
    Здравствуйте, {user.username}!

    Добро пожаловать в Blogicum - платформу для ведения блогов!

    Вы можете:
    - Создавать и публиковать посты
    - Комментировать публикации других пользователей
    - Настраивать свой профиль

    С уважением,
    Команда Blogicum
    '''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'registration/profile_edit.html', {'form': form})
