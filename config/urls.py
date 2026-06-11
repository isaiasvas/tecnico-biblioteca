from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
 
from livros.views import AutorViewSet, EditoraViewSet, CategoriaViewSet, LivroViewSet
from usuarios.views import EnderecoViewSet, UsuarioViewSet
from emprestimos.views import EmprestimoViewSet
 
router = DefaultRouter()
 
# Livros
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'editoras', EditoraViewSet, basename='editora')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'livros', LivroViewSet, basename='livro')
 
# Usuários
router.register(r'enderecos', EnderecoViewSet, basename='endereco')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
 
# Empréstimos
router.register(r'emprestimos', EmprestimoViewSet, basename='emprestimo')
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]