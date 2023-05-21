from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower', verbose_name='Автор рецепта')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following', verbose_name='Подписчики')

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [models.UniqueConstraint(
            fields=['author', 'following'], name='unique_subscribe')]

    def __str__(self):
        return f'{self.following.username} -> {self.author.username}'
