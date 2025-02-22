from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, MenuItem, Order, OrderItem, CateringOrder

# Custom Admin for CustomUser Model
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "phone", "address")}),
    )
    list_display = ("username", "email", "role", "phone", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "phone")

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# Admin for MenuItem
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "available")
    list_filter = ("category", "available")
    search_fields = ("name", "category__name")

# Admin for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "ordered_at", "status", "total_price")
    list_filter = ("status", "ordered_at")
    search_fields = ("customer__username", "customer__email")

# Admin for OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity", "price")
    search_fields = ("order__id", "menu_item__name")

# Admin for CateringOrder
class CateringOrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "event_type", "event_date", "quantity", "status")
    list_filter = ("event_type", "status")
    search_fields = ("customer__username", "event_type")
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address", "created_at")
    search_fields = ("user__username", "phone")
# Register models

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CateringOrder, CateringOrderAdmin)
