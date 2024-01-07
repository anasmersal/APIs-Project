from django.urls import path, include
from LittleLemonAPI import views

urlpatterns = [
    path("", include("djoser.urls")),
    path("menu-items/", views.multiple_items),
    path("menu-items/<int:id>", views.single_item),
    path("groups/manager/users/", views.managers),
    path("groups/manager/users/<int:user_id>", views.managers),
    path("groups/delivery_crew/users", views.delivery_crew),
    path("groups/delivery_crew/users/<int:user_id>", views.delivery_crew),
    path("cart/menu-items/", views.cart),
    path("orders/", views.order),
    path("orders/<int:id>", views.single_order),
]
