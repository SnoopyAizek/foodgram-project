from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет в HEX', null=True,
                             validators=[RegexValidator('^#([a-fA-F0-9]{6})',
                                                        message='Поле должно содержать HEX-код выбранного цвета.')])
    slug = models.CharField(max_length=200, unique=True, null=True, verbose_name='Уникальный идентификатор')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE, verbose_name='Автор')
    ingredients = models.ManyToManyField(
        Ingredient, through='Recipe_ingredient', through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты')
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='recipe_images/', blank=True, verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name='Время приготовления, мин')
    pub_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата публикации')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'author'], name='unique_for_author')]
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Recipe_ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes', verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(default=0, verbose_name='Количество', validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_combination')
            ]

    def __str__(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipe', verbose_name='Избранный рецепт')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,  related_name='favorite_user', verbose_name='Добавил в избранное')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_favorite')
            ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Shopping_cart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_recipe', verbose_name='Рецепт в корзине')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_user', verbose_name='Добавил в корзину')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_shopping_cart')
            ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
