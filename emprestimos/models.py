from django.db import models
from django.contrib.auth.models import User


class Emprestimo(models.Model):
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.PROTECT,
        related_name='emprestimo_ativo',
    )
    livro = models.ForeignKey(
        'livros.Livro',
        on_delete=models.PROTECT,
        related_name='emprestimos',
    )
    data_emprestimo = models.DateField(auto_now_add=True)
    data_limite = models.DateField()
    devolvido_at = models.DateField(null=True, blank=True)

    multa_atraso = models.FloatField(default=0.0, editable=False)
    multa_avaria = models.FloatField(default=0.0, editable=False)

    adicionado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='emprestimos_registrados',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Empréstimo de {self.usuario} — {self.livro}'

    def calcular_multa_atraso(self):
        from datetime import date
        referencia = self.devolvido_at or date.today()
        if referencia > self.data_limite:
            dias_atraso = (referencia - self.data_limite).days
            return round(dias_atraso * 1.0, 2) #corrigir isso para pegar o tipo e atraves do tipo você vai calcular o valor
        return 0.0

    def save(self, *args, **kwargs):
        self.multa_atraso = self.calcular_multa_atraso()
        super().save(*args, **kwargs)