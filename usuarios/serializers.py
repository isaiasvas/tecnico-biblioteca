from rest_framework import serializers
from usuarios.models import Endereco, Usuario

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = [
            'id',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'pais',
            'cep',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'adicionado_por', 'created_at', 'updated_at']


class UsuarioSerializer(serializers.ModelSerializer):
    enderecos_info = EnderecoSerializer(source='endereco', many=True, read_only=True)
    tipo_usuario_display = serializers.CharField(
        source='get_tipo_usuario_display', read_only=True
    )

    class Meta:
        model = Usuario
        fields = [
            'id',
            'nome_completo',
            'documento',
            'nascimento',
            'email',
            'telefone',
            'tipo_usuario',
            'tipo_usuario_display',
            'eh_ativo',
            'endereco',
            'enderecos_info',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'tipo_usuario_display',
            'enderecos_info',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]