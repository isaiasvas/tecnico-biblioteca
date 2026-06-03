#usuarios.admin
from django.contrib import admin
from .models import Endereco, Usuario


class AdicionadoPorMixin:
    readonly_fields = ('adicionado_por', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.adicionado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Endereco)
class EnderecoAdmin(AdicionadoPorMixin, admin.ModelAdmin):
    list_display = (
        'logradouro',
        'numero',
        'bairro',
        'cidade',
        'estado',
        'pais',
        'cep',
        'adicionado_por',
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

    fieldsets = (
        ('Localização', {
            'fields': (
                'logradouro',
                'numero',
                'complemento',
                'bairro',
                'cidade',
                'estado',
                'pais',
                'cep',
            ),
        }),
        ('Controle', {
            'fields': (
                'adicionado_por',
                'created_at',
                'updated_at',
            ),
        }),
    )


@admin.register(Usuario)
class UsuarioAdmin(AdicionadoPorMixin, admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'documento',
        'tipo_usuario',
        'eh_ativo',
        'email',
        'telefone',
        'nascimento',
        'adicionado_por',
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

    fieldsets = (
        ('Dados pessoais', {
            'fields': (
                'nome_completo',
                'documento',
                'nascimento',
                'email',
                'telefone',
            ),
        }),
        ('Perfil', {
            'fields': (
                'tipo_usuario',
                'eh_ativo',
                'endereco',
            ),
        }),
        ('Controle', {
            'fields': (
                'adicionado_por',
                'created_at',
                'updated_at',
            ),
        }),
    )