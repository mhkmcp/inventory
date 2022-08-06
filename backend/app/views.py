from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Inventory, InventoryGroup
from .serializers import InventorySerializer, InventoryGroupSerializer
from core.custom_method import IsAuthenticatedCustom


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.select_related('group', 'created_by')
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticatedCustom, )
    
    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)
    

class InventoryGroupView(ModelViewSet):
    queryset = InventoryGroup.objects.select_related('belongs_to', 'created_by').prefetch_related('inventories')
    serializer_class = InventoryGroupSerializer
    permission_classes = (IsAuthenticatedCustom, )
    
    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)