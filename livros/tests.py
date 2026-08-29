from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from livros.models import Autor, Categoria, Editora, Livro

API = '/api/v1/'


class LivroCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cat1', password='x12345678')
        self.categoria = Categoria.objects.create(nome='Tecnologia', adicionado_por=self.user)
        self.autor = Autor.objects.create(
            primeiro_nome='Clarice', ultimo_nome='Lispector', nascimento='1920-12-10',
            nacionalidade='Brasileira', adicionado_por=self.user,
        )
        self.editora = Editora.objects.create(
            nome='Rocco', publicado_at='2010-01-01', volume='1', edicao='1',
            adicionado_por=self.user,
        )
        self.client = APIClient()

    def auth(self):
        resp = self.client.post(
            f'{API}token/', {'username': 'cat1', 'password': 'x12345678'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def _livro_payload(self, isbn='9780000000100'):
        return {
            'titulo': 'Livro Teste', 'isbn': isbn, 'tipo_emprestimo': 'curto',
            'categoria': self.categoria.id, 'autor': [self.autor.id],
            'editora': [self.editora.id], 'paginas': '200', 'faixa_etaria': '12',
            'endereco': 'B-2', 'quantidade': '5', 'valor': 40,
        }

    def test_lista_sem_token_401(self):
        resp = self.client.get(f'{API}livros/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_criar_livro_vincula_adicionado_por(self):
        self.auth()
        resp = self.client.post(f'{API}livros/', self._livro_payload(), format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        livro = Livro.objects.get(isbn='9780000000100')
        self.assertEqual(livro.adicionado_por, self.user)
        self.assertEqual(livro.autor.count(), 1)
        self.assertEqual(livro.editora.count(), 1)

    def test_criar_livro_sem_isbn_valido_rejeitado(self):
        self.auth()
        payload = self._livro_payload(isbn='9780000000101')
        # isbn duplicado testa a unicidade
        self.client.post(f'{API}livros/', payload, format='json')
        resp = self.client.post(f'{API}livros/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('isbn', resp.data)
