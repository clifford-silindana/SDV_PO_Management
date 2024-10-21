from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Supplier, PurchaseOrder
from .serializers import SupplierSerializer, PurchaseOrderSerializer
from django.http import HttpResponse
import csv

@api_view(['GET', 'POST'])
def supplier_list(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def supplier_detail(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk = supplier_id)
    except Supplier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def purchase_order_list(request):
    if request.method == 'GET':
        orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, purchase_order_id):
    try:
        order = PurchaseOrder.objects.get(pk= purchase_order_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def send_purchase_order(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    purchase_order.status = 'sent'
    purchase_order.save()
    return Response({'status': 'Purchase order sent'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def export_purchase_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="purchase_orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['PO Number', 'Supplier', 'Status', 'Total Amount', 'Created At'])

    for purchase_order in PurchaseOrder.objects.all():
        writer.writerow([purchase_order.po_number, purchase_order.supplier.name, purchase_order.status, purchase_order.total_amount, purchase_order.created_at])

    return response

