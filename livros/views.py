from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from livros.models import Autor, Editora, Categoria, Livro
from .serializers import (
    AutorSerializer,
    EditoraSerializer,
    CategoriaSerializer,
    LivroSerializer,
)
from config.pagination import StandardPagination
from config.permissions import IsStaffOrReadOnly


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.select_related('adicionado_por').all()
    serializer_class = AutorSerializer
    ##permission_classes = [IsStaffOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['primeiro_nome', 'ultimo_nome', 'nacionalidade']
    ordering_fields = ['primeiro_nome', 'ultimo_nome', 'nascimento', 'created_at']
    ordering = ['primeiro_nome']


class EditoraViewSet(viewsets.ModelViewSet):
    queryset = Editora.objects.select_related('adicionado_por').all()
    serializer_class = EditoraSerializer
    #permission_classes = [IsStaffOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'publicado_at', 'created_at']
    ordering = ['nome']


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.select_related('parent', 'adicionado_por').all()
    serializer_class = CategoriaSerializer
    #permission_classes = [IsStaffOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['nome']
    filterset_fields = ['parent']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']


class LivroViewSet(viewsets.ModelViewSet):
    queryset = (
        Livro.objects
        .select_related('categoria', 'adicionado_por')
        .prefetch_related('autor', 'editora')
        .all()
    )
    serializer_class = LivroSerializer
    #permission_classes = [IsStaffOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['titulo', 'isbn', 'autor__primeiro_nome', 'autor__ultimo_nome']
    filterset_fields = ['categoria', 'tipo_emprestimo', 'autor', 'editora']
    ordering_fields = ['titulo', 'valor', 'created_at']
    ordering = ['titulo']
