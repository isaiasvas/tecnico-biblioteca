#usuarios.models

from django.db import models
from django.contrib.auth.models import User


class Endereco(models.Model):
    complemento = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='enderecos_adicionados',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['pais', 'estado', 'cidade']

    def __str__(self):
        return f'{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'


class Usuario(models.Model):

    class TipoUsuario(models.TextChoices):
        ALUNO = 'aluno', 'Aluno'
        FUNCIONARIO = 'funcionario', 'Funcionário'
        CONVIDADO = 'convidado', 'Convidado'

    nome_completo = models.CharField(max_length=50)
    documento = models.CharField(max_length=40, unique=True)
    nascimento = models.DateField()
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.ManyToManyField(
        Endereco,
        related_name='usuarios',
        blank=True,
    )
    eh_ativo = models.BooleanField(default=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.CONVIDADO,
    )

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='usuarios_adicionados',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome_completo']

    def __str__(self):
        return f'{self.nome_completo} ({self.get_tipo_usuario_display()})'