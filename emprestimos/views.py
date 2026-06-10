from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from emprestimos.models import Emprestimo
from .serializers import (
    EmprestimoSerializer,
    EmprestimoListSerializer,
    DevolucaoSerializer,
)
from config.pagination import StandardPagination
from config.permissions import IsAuthenticatedStaff

class EmprestimoViewSet(viewsets.ModelViewSet):
    """
    CRUD de empréstimos + action de devolução.

    POST /emprestimos/{id}/devolver/
        body: { "devolvido_at": "YYYY-MM-DD", "multa_avaria": 0.0 }
    """
    permission_classes = [IsAuthenticatedStaff]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = [
        'usuario__nome_completo',
        'usuario__documento',
        'livro__titulo',
        'livro__isbn',
    ]
    filterset_fields = ['usuario', 'livro', 'devolvido_at']
    ordering_fields = ['data_emprestimo', 'data_limite', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = (
            Emprestimo.objects
            .select_related('usuario', 'livro', 'adicionado_por')
            .all()
        )
        # Filtro rápido: ?ativo=true|false
        ativo = self.request.query_params.get('ativo')
        if ativo is not None:
            if ativo.lower() == 'true':
                qs = qs.filter(devolvido_at__isnull=True)
            elif ativo.lower() == 'false':
                qs = qs.filter(devolvido_at__isnull=False)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return EmprestimoListSerializer
        if self.action == 'devolver':
            return DevolucaoSerializer
        return EmprestimoSerializer

    # ------------------------------------------------------------------
    # Action: POST /emprestimos/{id}/devolver/
    # ------------------------------------------------------------------
    @action(detail=True, methods=['post'], url_path='devolver')
    def devolver(self, request, pk=None):
        emprestimo = self.get_object()

        if emprestimo.devolvido_at is not None:
            return Response(
                {'detail': 'Este empréstimo já foi devolvido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DevolucaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emprestimo.devolvido_at = serializer.validated_data['devolvido_at']
        emprestimo.multa_avaria = serializer.validated_data['multa_avaria']
        emprestimo.save()  # recalcula multa_atraso via model.save()

        return Response(
            EmprestimoSerializer(emprestimo, context={'request': request}).data,
            status=status.HTTP_200_OK,
        )

    # ------------------------------------------------------------------
    # Action: GET /emprestimos/em-atraso/
    # ------------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='em-atraso')
    def em_atraso(self, request):
        from datetime import date
        qs = self.get_queryset().filter(
            devolvido_at__isnull=True,
            data_limite__lt=date.today(),
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = EmprestimoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = EmprestimoListSerializer(qs, many=True)
        return Response(serializer.data)
