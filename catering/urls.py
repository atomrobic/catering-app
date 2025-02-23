from django.contrib import admin
from django.urls import path
from myapp.views import register, user_login, user_logout, user_profile, update_profile,catering_home,place_catering_order,admin_catering_orders,update_order_status,add_menu_item,delete_menu_item,menu_view_category,edit_menu_item
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", user_profile, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
    path("home", catering_home, name="catering_home"),
    path("place-order/", place_catering_order, name="place_catering_order"),
     path("adminorders/", admin_catering_orders, name="admin_catering_orders"),
    path("admin/orders/update/<int:order_id>/", update_order_status, name="update_order_status"),
    path('', add_menu_item, name='add_menu_item'),
    path("menu/delete/<int:item_id>/", delete_menu_item, name="delete_menu_item"),
     path('menuadd/', menu_view_category, name='menu_view_category'),
     path('menu/edit/<int:item_id>/', edit_menu_item, name="edit_menu_item"),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
