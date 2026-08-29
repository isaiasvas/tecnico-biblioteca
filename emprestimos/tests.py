from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from usuarios.models import Usuario
from livros.models import Autor, Categoria, Livro
from emprestimos.models import Emprestimo

API = '/api/v1/'


class EmprestimoMultaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='op1', password='x12345678')
        self.staff = User.objects.create_user(
            username='staff', password='x12345678', is_staff=True
        )
        self.usuario = Usuario.objects.create(
            user=self.staff, nome_completo='Leitor',
            documento='111.222.333-88', nascimento='1990-01-01',
        )
        self.categoria = Categoria.objects.create(
            nome='Tecnologia', adicionado_por=self.user
        )
        self.autor = Autor.objects.create(
            primeiro_nome='Machado', ultimo_nome='de Assis',
            nascimento='1839-06-21', nacionalidade='Brasileira',
            adicionado_por=self.user,
        )
        self.livro = Livro.objects.create(
            titulo='Livro Unico', isbn='9780000000001', tipo_emprestimo='unico',
            categoria=self.categoria, paginas='100', faixa_etaria='12',
            endereco='A-1', quantidade='3', valor=30, adicionado_por=self.user,
        )
        self.livro.autor.set([self.autor])
        self.client = APIClient()

    def auth(self):
        resp = self.client.post(
            f'{API}token/', {'username': 'op1', 'password': 'x12345678'},
            format='json',
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}"
        )

    def test_multa_atraso_usa_valor_por_tipo(self):
        self.auth()
        resp = self.client.post(
            f'{API}emprestimos/',
            {
                'usuario': self.usuario.id,
                'livro': self.livro.id,
                'data_limite': (date.today() - timedelta(days=2)).isoformat(),
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Tipo 'unico' => 5.00/dia x 2 dias = 10.00
        self.assertEqual(resp.data['multa_atraso'], 10.0)

    def test_devolucao_aplica_multa_avaria(self):
        self.auth()
        emp = Emprestimo.objects.create(
            usuario=self.usuario, livro=self.livro,
            data_limite=date.today() + timedelta(days=10),
            adicionado_por=self.user,
        )
        resp = self.client.post(
            f'{API}emprestimos/{emp.id}/devolver/',
            {'devolvido_at': date.today().isoformat(), 'multa_avaria': 2.5},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        emp.refresh_from_db()
        self.assertEqual(emp.multa_avaria, 2.5)
        self.assertIsNotNone(emp.devolvido_at)

    def test_usuario_pode_ter_novo_emprestimo_apos_devolver(self):
        self.auth()
        emp1 = Emprestimo.objects.create(
            usuario=self.usuario, livro=self.livro,
            data_limite=date.today() + timedelta(days=10),
            adicionado_por=self.user,
        )
        self.client.post(
            f'{API}emprestimos/{emp1.id}/devolver/',
            {'devolvido_at': date.today().isoformat(), 'multa_avaria': 0},
            format='json',
        )
        resp = self.client.post(
            f'{API}emprestimos/',
            {
                'usuario': self.usuario.id,
                'livro': self.livro.id,
                'data_limite': (date.today() + timedelta(days=5)).isoformat(),
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_nao_permite_dois_emprestimos_ativos(self):
        self.auth()
        Emprestimo.objects.create(
            usuario=self.usuario, livro=self.livro,
            data_limite=date.today() + timedelta(days=10),
            adicionado_por=self.user,
        )
        resp = self.client.post(
            f'{API}emprestimos/',
            {
                'usuario': self.usuario.id,
                'livro': self.livro.id,
                'data_limite': (date.today() + timedelta(days=5)).isoformat(),
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def _cria_usuario(self, nome):
        return Usuario.objects.create(
            user=None, nome_completo=nome,
            documento=f'doc-{nome.replace(" ", "-")}', nascimento='1990-01-01',
        )

    def test_nao_permite_emprestar_sem_disponibilidade(self):
        self.auth()
        livro_unico = Livro.objects.create(
            titulo='Livro Unico 1', isbn='9780000000002', tipo_emprestimo='unico',
            categoria=self.categoria, paginas='100', faixa_etaria='12',
            endereco='A-1', quantidade='1', valor=30, adicionado_por=self.user,
        )
        livro_unico.autor.set([self.autor])
        # Confirma que a criacao inicializou a disponibilidade = total.
        self.assertEqual(livro_unico.quantidade_disponivel, 1)

        outro = self._cria_usuario('Outro Leitor')

        # Primeiro empréstimo consome a única unidade.
        resp1 = self.client.post(
            f'{API}emprestimos/',
            {
                'usuario': self.usuario.id,
                'livro': livro_unico.id,
                'data_limite': (date.today() + timedelta(days=5)).isoformat(),
            },
            format='json',
        )
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)
        livro_unico.refresh_from_db()
        self.assertEqual(livro_unico.quantidade_disponivel, 0)

        # Segunda pessoa não consegue emprestar a mesma unidade.
        resp2 = self.client.post(
            f'{API}emprestimos/',
            {
                'usuario': outro.id,
                'livro': livro_unico.id,
                'data_limite': (date.today() + timedelta(days=5)).isoformat(),
            },
            format='json',
        )
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

        # Após devolver, volta a ter disponibilidade.
        emp = Emprestimo.objects.get(id=resp1.data['id'])
        dev = self.client.post(
            f'{API}emprestimos/{emp.id}/devolver/',
            {'devolvido_at': date.today().isoformat(), 'multa_avaria': 0},
            format='json',
        )
        self.assertEqual(dev.status_code, status.HTTP_200_OK)
        livro_unico.refresh_from_db()
        self.assertEqual(livro_unico.quantidade_disponivel, 1)

        # E a segunda pessoa consegue emprestar agora.
        resp3 = self.client.post(
            f'{API}emprestimos/',
            {
                'usuario': outro.id,
                'livro': livro_unico.id,
                'data_limite': (date.today() + timedelta(days=5)).isoformat(),
            },
            format='json',
        )
        self.assertEqual(resp3.status_code, status.HTTP_201_CREATED)
