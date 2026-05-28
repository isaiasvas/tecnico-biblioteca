# admin.py

from django.contrib import admin
from .models import Autor, Editora, Categoria, Livro


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = (
        'primeiro_nome',
        'ultimo_nome',
        'nacionalidade',
        'nascimento',
        'obito',
    )

    search_fields = (
        'primeiro_nome',
        'ultimo_nome',
        'nacionalidade',
    )

    list_filter = (
        'nacionalidade',
    )


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'publicado_at',
        'volume',
        'edicao',
    )

    search_fields = (
        'nome',
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'parent',
        'created_at',
    )

    search_fields = (
        'nome',
    )

    list_filter = (
        'parent',
    )


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'isbn',
        'categoria',
        'paginas',
        'faixa_etaria',
        'quantidade',
    )

    search_fields = (
        'titulo',
        'isbn',
    )

    list_filter = (
        'categoria',
    )

    filter_horizontal = (
        'autor',
        'editora',
    )