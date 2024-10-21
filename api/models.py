from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.po_number

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, help_text="e.g., piece, kg, box")
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class OrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.description



