from django.urls import path
from . import views

urlpatterns = [
    path('retrieve/suppliers/', views.supplier_list, name='supplier-list'),
    path('retrieve/suppliers/<int:supplier_id>/', views.supplier_detail, name='supplier-detail'),

    path('retrieve/purchase-orders/', views.purchase_order_list, name='purchase-order-list'),
    path('retrieve/purchase-orders/<int:purchase_order_id>/', views.purchase_order_detail, name='purchase-order-detail'),

    path('create/purchase-orders/<int:pk>/send/', views.send_purchase_order, name='send-purchase-order'),

    path('retrieve/purchase-orders/export-csv/', views.export_purchase_orders_csv, name='export-purchase-orders-csv'),
]
