from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class StaticPage(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    slug = models.SlugField(unique=True, verbose_name='URL-адрес')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, verbose_name='Автор'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'статичная страница'
        verbose_name_plural = 'Статичные страницы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
