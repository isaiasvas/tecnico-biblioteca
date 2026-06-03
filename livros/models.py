#livros.models
from django.db import models
from django.contrib.auth.models import User


class Autor(models.Model):
    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    nascimento = models.DateField()
    obito = models.DateField(null=True, blank=True)
    nacionalidade = models.CharField(max_length=100)

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='autores_adicionados',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['primeiro_nome', 'ultimo_nome']

    def __str__(self):
        return f'{self.primeiro_nome} {self.ultimo_nome}'


class Editora(models.Model):
    nome = models.CharField(max_length=100)
    publicado_at = models.DateField(verbose_name='Publicado Quando')
    volume = models.CharField(max_length=4, null=True, blank=True)
    edicao = models.CharField('Edição', max_length=30, null=True, blank=True)

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='editoras_adicionadas',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        verbose_name='Categoria Pai',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategorias',
    )

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='categorias_adicionadas',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        if self.parent:
            return f'{self.parent} > {self.nome}'
        return self.nome


class Livro(models.Model):

    class TipoEmprestimo(models.TextChoices):
        LONGO = 'longo', 'Longo'
        MEDIO = 'medio', 'Médio'
        CURTO = 'curto', 'Curto'
        UNICO = 'unico', 'Único'

    tipo_emprestimo = models.CharField(
        'Tipo de Empréstimo',
        max_length=20,
        choices=TipoEmprestimo.choices,
    )

    titulo = models.CharField(max_length=100)
    isbn = models.CharField(max_length=14, unique=True)

    autor = models.ManyToManyField(
        Autor,
        related_name='livros',
    )

    editora = models.ManyToManyField(
        Editora,
        related_name='livros',
    )

    paginas = models.CharField(max_length=4)
    faixa_etaria = models.CharField(max_length=3)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='livros',
    )

    endereco = models.CharField(max_length=30)
    quantidade = models.CharField(max_length=4)
    valor = models.FloatField('Valor do Livro (R$)', default=0.0)

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='livros_adicionados',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo