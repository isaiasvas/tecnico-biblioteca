from rest_framework.permissions import BasePermission, SAFE_METHODS
 
 
class IsStaffOrReadOnly(BasePermission):
    """
    Leitura liberada para autenticados.
    Escrita (POST, PUT, PATCH, DELETE) apenas para staff.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user
 
 
class IsAuthenticatedStaff(BasePermission):
    """
    Apenas staff autenticado tem acesso total.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
 