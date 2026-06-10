from rest_framework.routers import DefaultRouter
from .views import EmprestimoViewSet

router = DefaultRouter()
router.register('emprestimos', EmprestimoViewSet, basename='emprestimo')

urlpatterns = router.urls
