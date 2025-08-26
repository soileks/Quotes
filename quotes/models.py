from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Source(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('series', 'Сериал'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"


class Quote(models.Model):
    text = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)
    views_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['text', 'source']  # ✅ Дубликаты запрещены

    def clean(self):
        # ✅ Не больше 3 цитат у источника
        if self.pk is None:  # Только для новых записей
            if Quote.objects.filter(source=self.source).count() >= 3:
                raise ValidationError({'text': f"У одного источника не может быть больше 3 цитат"})

        if self.pk is None:  # Только для новых записей
            duplicate = Quote.objects.filter(text=self.text, source=self.source).first()
            if duplicate:
                raise ValidationError({
                    'text': f"Такая цитата уже существует для этого источника (ID: {duplicate.id})"
                })

    def save(self, *args, **kwargs):
        try:
            self.clean()  # ✅ Вызываем проверку перед сохранением
            super().save(*args, **kwargs)

        except ValidationError as e:
            # Перебрасываем ValidationError для forms
            raise e

        except IntegrityError as e:
            # Ловим ошибку уникальности из базы данных
            if 'unique together' in str(e).lower():
                raise ValidationError({
                    'text': "Такая цитата уже существует для этого источника. Дубликаты запрещены."
                })
            else:
                raise e

    def __str__(self):
        return f"{self.text[:50]}..."

    @property
    def rating(self):
        return self.likes - self.dislikes