from rest_framework.permissions import BasePermission
from rest_framework.views import exception_handler
from rest_framework.response import Response

from .utils import decodeJWT

class IsAuthenticatedCustom(BasePermission):
    
    def has_permission(self, request, view):
        try:
            auth_token = request.Meta.get("HTTP_AUTHORIZATION", None)
        except Exception:
            return False
        
        if not auth_token:
            return False 
    
        user = decodeJWT(auth_token)
        
        if not user:
            return False
        
        request.user = user
        return True
    

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        return response
    
    exc_list = str(exc).split("DETAIL: ")
    return Response({"error": exc_list[-1]}, status=403)