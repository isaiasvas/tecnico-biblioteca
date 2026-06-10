from rest_framework.routers import DefaultRouter
from .views import EnderecoViewSet, UsuarioViewSet

router = DefaultRouter()
router.register('enderecos', EnderecoViewSet, basename='endereco')
router.register('usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = router.urls
