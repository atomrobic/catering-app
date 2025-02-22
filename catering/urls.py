from django.contrib import admin
from django.urls import path
from myapp.views import register, user_login, user_logout, user_profile, update_profile,catering_home,place_catering_order,admin_catering_orders,update_order_status,admin_menu_view,add_menu_item
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", user_profile, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
    path("", catering_home, name="catering_home"),
    path("place-order/", place_catering_order, name="place_catering_order"),
     path("adminorders/", admin_catering_orders, name="admin_catering_orders"),
    path("admin/orders/update/<int:order_id>/", update_order_status, name="update_order_status"),
     path("menu_food/", admin_menu_view, name="admin_menu_view"),
    path('menu/add/', add_menu_item, name='add_menu_item'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
