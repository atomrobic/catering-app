from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ADMIN = "admin"
    CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (CUSTOMER, "Customer"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer_profile")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_items")
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add price field

    def __str__(self):
        return f"{self.name} ({'Available' if self.available else 'Not Available'})"

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Make sure this field is present


    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order {self.order.id})"

class CateringOrder(models.Model):
    EVENT_TYPES = [
        ("wedding", "Wedding"),
        ("birthday", "Birthday"),
        ("corporate", "Corporate Event"),
        ("House farming", "House farming"),
        ("other event","other event"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="catering_orders")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_date = models.DateField()
    photo = models.ImageField(upload_to="order_photos/", null=True, blank=True)
    quantity = models.PositiveIntegerField()
    menu_items = models.ManyToManyField(MenuItem)
    address = models.TextField(help_text="Event venue or delivery location")  # New field for delivery location
    special_requests = models.TextField(blank=True, null=True)  # Optional field for additional instructions
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Calculate based on menu items
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        """Calculate the total price based on selected menu items and quantity"""
        total = sum(item.price for item in self.menu_items.all()) * self.quantity
        self.total_price = total
        self.save()

    def __str__(self):
        return f"{self.customer.username} - {self.event_type} on {self.event_date} ({self.status})"

