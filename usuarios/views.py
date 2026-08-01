from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from usuarios.models import Endereco, Usuario
from .serializers import EnderecoSerializer, UsuarioSerializer
from config.pagination import StandardPagination
from config.permissions import IsStaffOrReadOnly, IsAuthenticatedStaff


class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.select_related('adicionado_por').all()
    serializer_class = EnderecoSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['logradouro', 'bairro', 'cidade', 'estado', 'cep']
    ordering_fields = ['cidade', 'estado', 'created_at']
    ordering = ['pais', 'estado', 'cidade']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(adicionado_por=self.request.user)
        else:
            serializer.save()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.prefetch_related('endereco').all()
    serializer_class = UsuarioSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['nome_completo', 'documento', 'email']
    filterset_fields = ['tipo_usuario', 'eh_ativo']
    ordering_fields = ['nome_completo', 'created_at']
    ordering = ['nome_completo']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(adicionado_por=self.request.user)
        else:
            serializer.save()