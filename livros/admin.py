#livros.admin
from django.contrib import admin
from .models import Autor, Editora, Categoria, Livro


class AdicionadoPorMixin:
    readonly_fields = ('adicionado_por', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.adicionado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Autor)
class AutorAdmin(AdicionadoPorMixin, admin.ModelAdmin):
    list_display = (
        'primeiro_nome',
        'ultimo_nome',
        'nacionalidade',
        'nascimento',
        'obito',
        'adicionado_por',
    )

    search_fields = (
        'primeiro_nome',
        'ultimo_nome',
        'nacionalidade',
    )

    list_filter = (
        'nacionalidade',
    )

    fieldsets = (
        ('Dados pessoais', {
            'fields': (
                'primeiro_nome',
                'ultimo_nome',
                'nascimento',
                'obito',
                'nacionalidade',
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


@admin.register(Editora)
class EditoraAdmin(AdicionadoPorMixin, admin.ModelAdmin):
    list_display = (
        'nome',
        'publicado_at',
        'volume',
        'edicao',
        'adicionado_por',
    )

    search_fields = (
        'nome',
    )

    fieldsets = (
        ('Dados da editora', {
            'fields': (
                'nome',
                'publicado_at',
                'volume',
                'edicao',
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


@admin.register(Categoria)
class CategoriaAdmin(AdicionadoPorMixin, admin.ModelAdmin):
    list_display = (
        'nome',
        'parent',
        'adicionado_por',
        'created_at',
    )

    search_fields = (
        'nome',
    )

    list_filter = (
        'parent',
    )

    fieldsets = (
        ('Dados da categoria', {
            'fields': (
                'nome',
                'parent',
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


@admin.register(Livro)
class LivroAdmin(AdicionadoPorMixin, admin.ModelAdmin):
    list_display = (
        'titulo',
        'isbn',
        'tipo_emprestimo',
        'valor',
        'categoria',
        'paginas',
        'faixa_etaria',
        'quantidade',
        'adicionado_por',
    )

    search_fields = (
        'titulo',
        'isbn',
    )

    list_filter = (
        'tipo_emprestimo',
        'categoria',
    )

    filter_horizontal = (
        'autor',
        'editora',
    )

    fieldsets = (
        ('Dados do livro', {
            'fields': (
                'titulo',
                'isbn',
                'paginas',
                'faixa_etaria',
                'endereco',
                'quantidade',
                'valor',
            ),
        }),
        ('Empréstimo', {
            'fields': (
                'tipo_emprestimo',
            ),
        }),
        ('Relações', {
            'fields': (
                'autor',
                'editora',
                'categoria',
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