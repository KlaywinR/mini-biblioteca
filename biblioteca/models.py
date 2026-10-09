from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=120)
    nationality = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books",
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="books",
    )
    year_of_publication = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
