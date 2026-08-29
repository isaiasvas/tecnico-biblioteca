from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from usuarios.models import Endereco, Usuario
from .serializers import (
    EnderecoSerializer,
    UsuarioSerializer,
    UsuarioRegisterSerializer,
)
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
        with transaction.atomic():
            serializer.save(
                adicionado_por=self.request.user
                if self.request.user.is_authenticated
                else None
            )

    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        refresh = RefreshToken.for_user(usuario.user)
        return Response(
            {
                'usuario': UsuarioSerializer(
                    usuario, context={'request': request}
                ).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


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