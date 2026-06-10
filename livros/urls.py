from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, EditoraViewSet, CategoriaViewSet, LivroViewSet

router = DefaultRouter()
router.register('autores', AutorViewSet, basename='autor')
router.register('editoras', EditoraViewSet, basename='editora')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('livros', LivroViewSet, basename='livro')

urlpatterns = router.urls
