from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user_control.models import UserActivities

from .views import (
    ShopView,
    SummaryView,
    InvoiceView,
    Purchaseview,
    InventoryView,
    SaleByShopView,
    InventoryGroupView,
    SalePerformanceView,
    InventoryCSVLoaderView,
)


router = DefaultRouter(trailing_slash=False)
router.register("inventory", InventoryView, 'inventory')
router.register("inventory-csv", InventoryCSVLoaderView, 'inventory-csv')
router.register("shop", ShopView, 'shop')
router.register("summary", SummaryView, 'summary')
router.register("sales-by-sop", SaleByShopView, 'sales-by-shop')
router.register("group", InventoryGroupView, 'group')
router.register("top-selling", SalePerformanceView, 'top-selling')
router.register("invoice", InvoiceView, 'users')
router.register("purchase-summary", Purchaseview, 'purchase-summary')


urlpatterns = [
    path("", include(router.urls)),
]
