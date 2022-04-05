from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    RED = '#FF0000'
    YELLOW = '#FFFF00'
    ORANGE = '#FFA500'
    PINK = '#FF1493'
    PURPLE = '#800080'
    GREEN = '#008000'
    COLOR_CHOICE = [
        (RED, 'Красный'),
        (YELLOW, 'Желтый'),
        (ORANGE, 'Оранжевый'),
        (PINK, 'Розовый'),
        (PURPLE, 'Фиолетовый'),
        (GREEN, 'Зеленый')
    ]
    name = models.CharField(
        verbose_name='Название тега', unique=True,
        blank=True, max_length=256
    )
    color = models.CharField(
        choices=COLOR_CHOICE, max_length=8, unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        unique=True, max_length=256, verbose_name='Слаг тега'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}, цвет {self.color}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=256, verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='NumberOfIngredients',
        verbose_name='Кол-во ингредиентов'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Фото рецепта'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время говтоки',
        default=1,
        validators=[MinValueValidator(1, 'Время готовки не может быть меньше 1')]
    )
    pub_date = models.DateField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class NumberOfIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Минимальное кол-во равно 1')],
        default=1, verbose_name='Количество'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.amount} в таком рецепте: {self.recipe}'

