from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Article(models.Model):
    """ Модель для сущности Статья """
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение')
    count_views = models.SmallIntegerField(verbose_name='Количество просмотров')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title}/{self.count_views}/{self.date_published}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
