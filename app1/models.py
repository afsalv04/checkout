from django.db import models
from django.contrib.auth.models import User


# Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, blank=True, null=True)
    stock = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to="product/")

    def __str__(self):
        return f"{self.name} ({self.brand})"


# User Profile (extra details for user)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=225)
    address_line2 = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


# Contact Us
class ContactUs(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


# Cart Item
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# Billing Details
class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    apartment = models.CharField(max_length=200, blank=True, null=True)
    state_country = models.CharField(max_length=100)
    postal_zip = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    order_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Order
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('bank', 'Direct Bank Transfer'),
        ('cheque', 'Cheque Payment'),
        ('paypal', 'Paypal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing = models.ForeignKey(BillingDetails, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total(self):
        return self.subtotal


# Order Items
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
