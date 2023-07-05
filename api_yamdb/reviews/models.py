from django.db import models

from .validators import validate_year_release

TITLE_DATA = '{name}, {year}, {description}, {category}, {genre}'


class Categorie(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Метка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Введите название жанра'
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Метка')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения (определённый фильм, книга или песенка)."""
    name = models.CharField(
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска', validators=[validate_year_release]
    )
    description = models.TextField(verbose_name='Описание произведения')
    category = models.ForeignKey(
        Categorie,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория, к которому относиться произведение'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name='Жанр',
        help_text='Жанры, к которым относиться произведение'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return TITLE_DATA.format(
            name=self.name,
            year=self.year,
            description=self.description,
            category=self.category,
            genre=self.genre
        )


class GenreTitle(models.Model):
    """Модель связи id произведения и id жанра."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
