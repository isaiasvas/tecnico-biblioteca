from django.core.management.base import BaseCommand
from faker import Faker
import random

from livros.models import Autor, Editora, Categoria, Livro

fake = Faker('pt_BR')

class Command(BaseCommand):
    help = 'Popula o banco com dados fictícios'

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.WARNING('Apagando dados antigos...'))

        Livro.objects.all().delete()
        Autor.objects.all().delete()
        Editora.objects.all().delete()
        Categoria.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Criando categorias...'))

        tecnologia = Categoria.objects.create(nome='Tecnologia')

        programacao = Categoria.objects.create(
            nome='Programação',
            parent=tecnologia
        )

        python_categoria = Categoria.objects.create(
            nome='Python',
            parent=programacao
        )

        self.stdout.write(self.style.SUCCESS('Criando autores...'))

        autores = []

        for _ in range(50):
            autor = Autor.objects.create(
                primeiro_nome=fake.first_name(),
                ultimo_nome=fake.last_name(),
                nascimento=fake.date_of_birth(minimum_age=30, maximum_age=90),
                nacionalidade='Brasileira'
            )

            autores.append(autor)

        self.stdout.write(self.style.SUCCESS('Criando editoras...'))

        editoras = []

        for i in range(35):
            editora = Editora.objects.create(
                nome=f'Editora {i + 1}',
                publicado_at=fake.date_this_decade(),
                volume=str(random.randint(1, 9)),
                edicao=f'{random.randint(1, 10)}ª edição'
            )

            editoras.append(editora)

        self.stdout.write(self.style.SUCCESS('Criando livros...'))

        for i in range(20):

            livro = Livro.objects.create(
                titulo=fake.sentence(nb_words=3),
                isbn=fake.unique.isbn13(separator=''),
                paginas=str(random.randint(100, 900)),
                faixa_etaria=str(random.randint(10, 18)),
                categoria=python_categoria,
                endereco=f'A-{random.randint(1, 50)}',
                quantidade=str(random.randint(1, 20))
            )

            livro.autor.set(random.sample(autores, random.randint(1, 3)))
            livro.editora.set(random.sample(editoras, random.randint(1, 2)))

        self.stdout.write(
            self.style.SUCCESS('Banco populado com sucesso!')
        )