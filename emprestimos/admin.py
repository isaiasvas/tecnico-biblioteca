#emprestimos.admin
from django.contrib import admin
from .models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'livro',
        'data_emprestimo',
        'data_limite',
        'devolvido_at',
        'multa_atraso',
        'multa_avaria',
        'adicionado_por',
    )

    search_fields = (
        'usuario__nome',
        'livro__titulo',
        'adicionado_por__username',
    )

    list_filter = (
        'devolvido_at',
        'data_limite',
        'adicionado_por',
    )

    readonly_fields = (
        'data_emprestimo',
        'multa_atraso',
        'multa_avaria',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Dados do empréstimo', {
            'fields': (
                'usuario',
                'livro',
                'data_emprestimo',
                'data_limite',
                'devolvido_at',
            ),
        }),
        ('Multas', {
            'fields': (
                'multa_atraso',
                'multa_avaria',
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

    def save_model(self, request, obj, form, change):
        if not change:
            obj.adicionado_por = request.user
        super().save_model(request, obj, form, change)