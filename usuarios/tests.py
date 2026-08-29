from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from usuarios.models import Usuario

API = '/api/v1/'


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_cria_user_e_usuario_linkados(self):
        resp = self.client.post(
            f'{API}register/',
            {
                'nome_completo': 'Maria Silva',
                'documento': '111.222.333-44',
                'nascimento': '1995-05-05',
                'email': 'maria@example.com',
                'telefone': '11999999999',
                'username': 'maria_silva',
                'password': 'senha-segura-123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

        usuario = Usuario.objects.get(documento='111.222.333-44')
        self.assertIsNotNone(usuario.user)
        user = User.objects.get(username='maria_silva')
        self.assertEqual(usuario.user, user)
        # A senha deve estar com hash do Django.
        self.assertNotEqual(user.password, 'senha-segura-123')
        self.assertTrue(user.check_password('senha-segura-123'))

    def test_register_sem_username_duplicado(self):
        self.client.post(
            f'{API}register/',
            {
                'nome_completo': 'Ana',
                'documento': '111.222.333-55',
                'nascimento': '1995-05-05',
                'username': 'ana_um',
                'password': 'senha-segura-123',
            },
            format='json',
        )
        resp = self.client.post(
            f'{API}register/',
            {
                'nome_completo': 'Ana Dois',
                'documento': '999.888.777-66',
                'nascimento': '1996-06-06',
                'username': 'ana_um',
                'password': 'outra-senha-123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', resp.data)


class AuthProtectionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='senha123'
        )
        self.client = APIClient()

    def test_endpoint_protegido_retorna_401_sem_token(self):
        resp = self.client.get(f'{API}usuarios/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_endpoint_protegido_com_token_ok(self):
        user = User.objects.create_user(username='u2', password='x12345678')
        Usuario.objects.create(
            user=user, nome_completo='Fulano',
            documento='111.222.333-77', nascimento='1990-01-01',
        )
        resp = self.client.post(
            f'{API}token/', {'username': 'u2', 'password': 'x12345678'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp2 = self.client.get(f'{API}usuarios/')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
