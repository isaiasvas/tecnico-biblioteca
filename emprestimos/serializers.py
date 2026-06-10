from rest_framework import serializers
from emprestimos.models import Emprestimo
from livros.models import Livro

MULTA_POR_TIPO = {
    Livro.TipoEmprestimo.UNICO: 5.00,   # Único – alta rotatividade
    Livro.TipoEmprestimo.CURTO: 3.00,   # Curto
    Livro.TipoEmprestimo.MEDIO: 2.00,   # Médio
    Livro.TipoEmprestimo.LONGO: 1.00,   # Longo
}

class EmprestimoSerializer(serializers.ModelSerializer):
    adicionado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())

    usuario_nome = serializers.StringRelatedField(source='usuario', read_only=True)
    livro_titulo = serializers.StringRelatedField(source='livro', read_only=True)
    livro_tipo_emprestimo = serializers.CharField(
        source='livro.tipo_emprestimo', read_only=True
    )
    esta_atrasado = serializers.SerializerMethodField()
    dias_atraso = serializers.SerializerMethodField()
    multa_total = serializers.SerializerMethodField()

    class Meta:
        model = Emprestimo
        fields = [
            'id',
            'usuario',
            'usuario_nome',
            'livro',
            'livro_titulo',
            'livro_tipo_emprestimo',
            'data_emprestimo',
            'data_limite',
            'devolvido_at',
            'multa_atraso',
            'multa_avaria',
            'multa_total',
            'esta_atrasado',
            'dias_atraso',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'usuario_nome',
            'livro_titulo',
            'livro_tipo_emprestimo',
            'data_emprestimo',
            'multa_atraso',
            'multa_avaria',
            'multa_total',
            'esta_atrasado',
            'dias_atraso',
            'created_at',
            'updated_at',
        ]

    def _dias_atraso(self, obj) -> int:
        from datetime import date
        referencia = obj.devolvido_at or date.today()
        if referencia > obj.data_limite:
            return (referencia - obj.data_limite).days
        return 0

    def get_esta_atrasado(self, obj) -> bool:
        return self._dias_atraso(obj) > 0

    def get_dias_atraso(self, obj) -> int:
        return self._dias_atraso(obj)

    def get_multa_total(self, obj) -> float:
        return round(obj.multa_atraso + obj.multa_avaria, 2)

    def validate(self, attrs):
        usuario = attrs.get('usuario', getattr(self.instance, 'usuario', None))
        livro = attrs.get('livro', getattr(self.instance, 'livro', None))

        if self.instance is None:  
            if Emprestimo.objects.filter(
                usuario=usuario, devolvido_at__isnull=True
            ).exists():
                raise serializers.ValidationError(
                    {'usuario': 'Este usuário já possui um empréstimo ativo.'}
                )

        data_limite = attrs.get('data_limite')
        if self.instance is None and data_limite is None:
            raise serializers.ValidationError(
                {'data_limite': 'Este campo é obrigatório.'}
            )

        return attrs

class EmprestimoListSerializer(serializers.ModelSerializer):
    """Versão compacta para listagem."""
    usuario_nome = serializers.StringRelatedField(source='usuario')
    livro_titulo = serializers.StringRelatedField(source='livro')
    multa_total = serializers.SerializerMethodField()

    class Meta:
        model = Emprestimo
        fields = [
            'id',
            'usuario_nome',
            'livro_titulo',
            'data_emprestimo',
            'data_limite',
            'devolvido_at',
            'multa_total',
        ]

    def get_multa_total(self, obj):
        return round(obj.multa_atraso + obj.multa_avaria, 2)

class DevolucaoSerializer(serializers.Serializer):
    """Serializer específico para registrar devolução e multa de avaria."""
    devolvido_at = serializers.DateField()
    multa_avaria = serializers.FloatField(min_value=0.0, default=0.0)

    def validate_devolvido_at(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError(
                'A data de devolução não pode ser no futuro.'
            )
        return value