from rest_framework import serializers
from livros.models import Autor, Editora, Categoria, Livro

class AutorSerializer(serializers.ModelSerializer):
    adicionado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Autor
        fields = [
            'id',
            'primeiro_nome',
            'ultimo_nome',
            'nascimento',
            'obito',
            'nacionalidade',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AutorResumoSerializer(serializers.ModelSerializer):
    """Versão compacta usada como nested em Livro."""
    class Meta:
        model = Autor
        fields = ['id', 'primeiro_nome', 'ultimo_nome']

class EditoraSerializer(serializers.ModelSerializer):
    adicionado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Editora
        fields = [
            'id',
            'nome',
            'publicado_at',
            'volume',
            'edicao',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EditoraResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = ['id', 'nome']

class CategoriaSerializer(serializers.ModelSerializer):
    adicionado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent_nome = serializers.StringRelatedField(source='parent', read_only=True)

    class Meta:
        model = Categoria
        fields = [
            'id',
            'nome',
            'parent',
            'parent_nome',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'parent_nome', 'created_at', 'updated_at']


class CategoriaResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class LivroSerializer(serializers.ModelSerializer):
    adicionado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Leitura: objetos expandidos
    autores_info = AutorResumoSerializer(source='autor', many=True, read_only=True)
    editoras_info = EditoraResumoSerializer(source='editora', many=True, read_only=True)
    categoria_info = CategoriaResumoSerializer(source='categoria', read_only=True)
    tipo_emprestimo_display = serializers.CharField(
        source='get_tipo_emprestimo_display', read_only=True
    )

    class Meta:
        model = Livro
        fields = [
            'id',
            'titulo',
            'isbn',
            'tipo_emprestimo',
            'tipo_emprestimo_display',
            'autor',          # IDs para escrita
            'autores_info',   # objetos para leitura
            'editora',
            'editoras_info',
            'categoria',
            'categoria_info',
            'paginas',
            'faixa_etaria',
            'endereco',
            'quantidade',
            'valor',
            'adicionado_por',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'autores_info',
            'editoras_info',
            'categoria_info',
            'tipo_emprestimo_display',
            'created_at',
            'updated_at',
        ]
