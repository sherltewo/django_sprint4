from django.db import models
from django.contrib.auth import get_user_model


class Category (models.Model):
    """
    Тематическая категория.
    Category
    """

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        unique=True,
        verbose_name='Описание'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text="Снимите галочку, чтобы скрыть публикацию."
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text="Идентификатор страницы для URL; "
        "разрешены символы латиницы, "
        "цифры, дефис и подчёркивание."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    """
    Географическая метка.
    Location
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text="Снимите галочку, чтобы скрыть публикацию."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


User = get_user_model()


class Post(models.Model):
    """
    Публикация.
    Post
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст',
        help_text="""
        """
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text="""
        Снимите галочку, чтобы скрыть публикацию.
        """
    )
    pub_date = models.DateTimeField(
        auto_now_add=False,
        verbose_name='Дата и время публикации',
        help_text="Если установить дату и время в будущем — можно делать "
        "отложенные публикации."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        verbose_name='Изображение публикации',
        help_text='Добавьте изображение к публикации'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Комментарий к публикации."""

    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']  # Сортировка от старых к новым

    def __str__(self):
        return f'Комментарий {self.author} к посту {self.post.id}'
