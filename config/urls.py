from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

api_v1 = [
    include('livros.urls'),
    include('usuarios.urls'),
    include('emprestimos.urls'),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticação JWT
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Recursos
    path('api/v1/', include('livros.urls')),
    path('api/v1/', include('usuarios.urls')),
    path('api/v1/', include('emprestimos.urls')),

    # Browsable API login (dev)
    path('api-auth/', include('rest_framework.urls')),
]
