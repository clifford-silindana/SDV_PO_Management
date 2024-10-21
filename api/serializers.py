from rest_framework import serializers
from .models import Supplier, PurchaseOrder, OrderItem

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total_price']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'supplier', 'created_at', 'status', 'total_amount', 'items']

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier')
        items_data = validated_data.pop('items')
        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        purchase_order = PurchaseOrder.objects.create(supplier=supplier, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(purchase_order=purchase_order, **item_data)
        return purchase_order

    def update(self, instance, validated_data):
        supplier_data = validated_data.pop('supplier', None)
        items_data = validated_data.pop('items', None)

        if supplier_data:
            supplier, created = Supplier.objects.get_or_create(**supplier_data)
            instance.supplier = supplier

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(purchase_order=instance, **item_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

