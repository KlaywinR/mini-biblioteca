from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Category

class ModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Machado de Assis")
        self.book = Book.objects.create(
            title="Dom Casmurro", author=self.author, year_of_publication=1899
        )

    def test_str(self):
        self.assertEqual(str(self.author), "Machado de Assis")
        self.assertEqual(str(self.book), "Dom Casmurro")
        self.assertEqual(str(Category.objects.create(name="Romance")), "Romance")

    def test_related_name_books(self):
        self.assertEqual(list(self.author.books.all()), [self.book])

    def test_book_pode_ficar_sem_categoria(self):
        self.assertEqual(self.book.categories.count(), 0)

    def test_nao_apaga_autor_com_livros(self):
        with self.assertRaises(ProtectedError):
            self.author.delete()
        self.assertTrue(Author.objects.filter(pk=self.author.pk).exists())

    def test_autor_sem_livros_pode_ser_apagado(self):
        outro = Author.objects.create(name="Sem Livros")
        outro.delete()
        self.assertFalse(Author.objects.filter(pk=outro.pk).exists())

class ViewTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Graciliano Ramos")
        Book.objects.create(title="Vidas Secas", author=self.author, year_of_publication=1938)

    def test_lista_tem_link_para_autor(self):
        response = self.client.get(reverse("book_list"))
        url = reverse("author_detail", args=[self.author.pk])
        self.assertContains(response, f'href="{url}"')

    def test_author_detail_lista_livros(self):
        response = self.client.get(reverse("author_detail", args=[self.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vidas Secas")

    def test_author_detail_404(self):
        response = self.client.get(reverse("author_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
