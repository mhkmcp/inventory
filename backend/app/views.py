from ast import keyword
from curses import keyname
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from .models import Inventory, InventoryGroup
from .serializers import InventorySerializer, InventoryGroupSerializer
from core.custom_method import IsAuthenticatedCustom
from core.utils import CustomPagination, get_query


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.select_related('group', 'created_by')
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = CustomPagination
    
    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        
        results = self.queryset(**data)
        if keyword:
            search_fields = (
                'code',
                'created_by__fullname',
                'created_by__email',
                'group__name',
                'name',
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results 
    
    
    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)
    

class InventoryGroupView(ModelViewSet):
    queryset = InventoryGroup.objects.select_related('belongs_to', 'created_by').prefetch_related('inventories')
    serializer_class = InventoryGroupSerializer
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = (CustomPagination, )
    
    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        
        results = self.queryset(**data)
        if keyword:
            search_fields = (
                'created_by__fullname',
                'created_by__email',
                'name',
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        return results.annotate(
            total_items = Count('inventories')
        )
    
    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)