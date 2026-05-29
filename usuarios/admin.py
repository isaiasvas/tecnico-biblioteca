from django.contrib import admin
from .models import Endereco, Usuario


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = (
        'logradouro',
        'numero',
        'bairro',
        'cidade',
        'estado',
        'pais',
        'cep',
    )

    search_fields = (
        'logradouro',
        'bairro',
        'cidade',
        'estado',
        'cep',
    )

    list_filter = (
        'pais',
        'estado',
        'cidade',
    )


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'documento',
        'tipo_usuario',
        'eh_ativo',
        'email',
        'telefone',
        'nascimento',
    )

    search_fields = (
        'nome_completo',
        'documento',
        'email',
    )

    list_filter = (
        'tipo_usuario',
        'eh_ativo',
    )

    filter_horizontal = (
        'endereco',
    )