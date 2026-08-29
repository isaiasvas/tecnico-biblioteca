from django.contrib.auth.models import User
from django.db import transaction
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

    # Credenciais de acesso. Apenas escritura: quando fornecidas, o sistema
    # cria (ou atualiza) o User do Django vinculado ao Usuario.
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    user_username = serializers.CharField(
        source='user.username', read_only=True, default=None
    )
    user_email = serializers.EmailField(
        source='user.email', read_only=True, default=None
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
            'user',
            'username',
            'password',
            'user_username',
            'user_email',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'tipo_usuario_display',
            'enderecos_info',
            'user',
            'user_username',
            'user_email',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if username and password:
            email = validated_data.get('email') or ''
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            validated_data['user'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        user = instance.user

        if username and instance.user is None:
            email = validated_data.get('email') or instance.email or ''
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password or User.objects.make_random_password(),
            )
            user.is_active = True
            user.save()
            instance.user = user

        elif user is not None:
            if username and username != user.username:
                user.username = username
                user.save()
            if email := (validated_data.get('email') or instance.email):
                user.email = email
                user.save()
            if password:
                user.set_password(password)
                user.save()

        return super().update(instance, validated_data)


class UsuarioRegisterSerializer(serializers.Serializer):
    """Cadastro público que cria User + Usuario em uma transação única."""

    nome_completo = serializers.CharField(max_length=50)
    documento = serializers.CharField(max_length=40)
    nascimento = serializers.DateField()
    email = serializers.EmailField(max_length=100, required=False, allow_blank=True)
    telefone = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        write_only=True, min_length=8, style={'input_type': 'password'}
    )

    def validate_documento(self, value):
        if Usuario.objects.filter(documento=value).exists():
            raise serializers.ValidationError('Já existe um usuário com este documento.')
        return value

    def validate_email(self, value):
        if value and Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Já existe um usuário com este e-mail.')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nome de usuário já está em uso.')
        return value

    def create(self, validated_data):
        email = validated_data.get('email') or ''
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=email,
                password=validated_data['password'],
            )
            usuario = Usuario.objects.create(
                user=user,
                nome_completo=validated_data['nome_completo'],
                documento=validated_data['documento'],
                nascimento=validated_data['nascimento'],
                email=email or None,
                telefone=validated_data.get('telefone') or None,
                tipo_usuario=Usuario.TipoUsuario.CONVIDADO,
                adicionado_por=user,
            )
        return usuario