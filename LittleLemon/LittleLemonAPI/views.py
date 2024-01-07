from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .serializers import (
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import MenuItem, Cart, Order, OrderItem
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from django.db import transaction


@api_view(["GET", "POST"])
def multiple_items(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            item = MenuItem.objects.all()
            # ordering = request.query_params.get("ordering")
            # perpage = request.query_params.get("perpage", default=2)
            # page = request.query_params.get("page", default=1)
            # if ordering:
            #     item = item.order_by(ordering)
            # paginator = Paginator(item, per_page=perpage)
            # try:
            #     item = paginator.page(number=page)
            # except EmptyPage:
            #     item = []
            serialized_item = MenuItemSerializer(item, many=True)
            return Response(serialized_item.data, status=status.HTTP_200_OK)
        if (
            request.method == "POST"
            and request.user.groups.filter(name="Manager").exists()
        ):
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "you're not allowed to add menuitem"},
                status=status.HTTP_403_FORBIDDEN,
            )

    else:
        return Response(
            {"message": "Anonymous user, login first"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET", "PUT", "DELETE", "PATCH"])
def single_item(request, id):
    if request.user.is_authenticated:
        if request.method == "GET":
            item = get_object_or_404(MenuItem, pk=id)
            serialized_item = MenuItemSerializer(item)
            return Response(serialized_item.data)

        if request.user.groups.filter(name="Manager").exists():
            if request.method == "DELETE":
                item = get_object_or_404(MenuItem, pk=id)
                item.delete()
                return Response(
                    {"message": "Menu item deleted"}, status=status.HTTP_204_NO_CONTENT
                )

            if request.method == "PUT":
                item = get_object_or_404(MenuItem, pk=id)
                serializer = MenuItemSerializer(item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if request.method == "PATCH":
                item = get_object_or_404(MenuItem, pk=id)
                serializer = MenuItemSerializer(item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "You're not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    else:
        return Response(
            {"message": "Anonymous user, login first"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET", "POST", "DELETE"])
def managers(request, user_id=None):
    # Check if the requesting user is in the "Manager" group
    if not request.user.groups.filter(name="Manager").exists():
        return Response(
            {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # For GET method to retrieve manager users
    if request.method == "GET" and not user_id:
        managers_group = Group.objects.get(name="Manager")
        manager_users = managers_group.user_set.all()
        serialized_users = [
            {"id": user.id, "username": user.username} for user in manager_users
        ]
        return Response(serialized_users, status=status.HTTP_200_OK)
    # For POST requests to add users to the "managers" group
    if request.method == "POST":
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": "Created"}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
        )

    # For DELETE requests to remove a user from the "managers" group by user ID
    if request.method == "DELETE" and user_id:
        user = get_object_or_404(User, pk=user_id)
        managers = Group.objects.get(name="Manager")
        if user in managers.user_set.all():
            managers.user_set.remove(user)
            return Response({"message": "User removed"}, status=status.HTTP_200_OK)
        return Response(
            {"message": "User not found in 'Manager' group"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
def delivery_crew(request, user_id=None):
    # Check if the requesting user is in the "Manager" group
    if not request.user.groups.filter(name="Manager").exists():
        return Response(
            {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # For GET method to retrieve manager users
    if request.method == "GET" and not user_id:
        managers_group = Group.objects.get(name="Delivery crew")
        delivery_users = managers_group.user_set.all()
        serialized_users = [
            {"id": user.id, "username": user.username} for user in delivery_users
        ]
        return Response(serialized_users, status=status.HTTP_200_OK)
    # For POST requests to add users to the "managers" group
    if request.method == "POST":
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            delivery = Group.objects.get(name="Delivery crew")
            delivery.user_set.add(user)
            return Response({"message": "Created"}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
        )

    # For DELETE requests to remove a user from the "managers" group by user ID
    if request.method == "DELETE" and user_id:
        user = get_object_or_404(User, pk=user_id)
        delivery = Group.objects.get(name="Delivery crew")
        if user in delivery.user_set.all():
            delivery.user_set.remove(user)
            return Response({"message": "User removed"}, status=status.HTTP_200_OK)
        return Response(
            {"message": "User not found in 'Delivery crew' group"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
def cart(request, user_id=None):
    if (
        request.user.is_authenticated
        and not request.user.groups.filter(name="Manager").exists()
        and not request.user.groups.filter(name="Delivery crew").exists()
    ):
        if request.method == "GET":
            # Filter Cart items for the current authenticated user
            items_in_cart = Cart.objects.filter(user=request.user)
            serialized_items = CartSerializer(items_in_cart, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)

        if request.method == "POST":
            # Create a mutable copy of the QueryDict
            cart_data = request.data.copy()
            # Set the 'user' field to the authenticated user's ID
            cart_data["user"] = request.user.id

            serializer = CartSerializer(data=cart_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "DELETE":
            # Filter cart items belonging to the current authenticated user
            cart_items_to_delete = Cart.objects.filter(user=request.user)
            # Delete the filtered cart items
            cart_items_to_delete.delete()

            return Response(
                {"message": "Cart items deleted"}, status=status.HTTP_200_OK
            )

    else:
        return Response(
            {"message": "Anonymous user, login first"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET", "POST", "DELETE"])
def order(request, user_id=None):
    if request.user.is_authenticated:
        if request.method == "GET":
            if request.user.groups.filter(name="Manager").exists():
                items_in_order = Order.objects.all()
                serialized_items = OrderSerializer(items_in_order, many=True)
                return Response(serialized_items.data, status=status.HTTP_200_OK)

            elif request.user.groups.filter(name="Delivery crew").exists():
                items_in_order = Order.objects.filter(delivery_crew=request.user)
                serialized_items = OrderSerializer(items_in_order, many=True)
                return Response(serialized_items.data, status=status.HTTP_200_OK)

            else:
                # Filter Cart items for the current authenticated user
                items_in_order = Order.objects.filter(user=request.user)
                serialized_items = OrderSerializer(items_in_order, many=True)
                return Response(serialized_items.data, status=status.HTTP_200_OK)

        if request.method == "POST":
            user = request.user

            if (
                not user.groups.filter(name="Manager").exists()
                and not user.groups.filter(name="Delivery crew").exists()
            ):
                # Retrieve cart items for the current user
                cart_items = Cart.objects.filter(user=user)

                # Calculate total price for the order
                total_price = sum(cart_item.price for cart_item in cart_items)

                # Create a new order for the user
                with transaction.atomic():
                    order = Order.objects.create(
                        user=user, total=total_price, date=date.today()
                    )

                    # Create OrderItem objects from cart items
                    order_items = [
                        OrderItem(
                            order=order,
                            menuitem=cart_item.menuitem,
                            quantity=cart_item.quantity,
                            unit_price=cart_item.unit_price,
                            price=cart_item.price,
                        )
                        for cart_item in cart_items
                    ]

                    # Bulk create OrderItem objects
                    OrderItem.objects.bulk_create(order_items)

                    # Delete cart items for the user
                    cart_items.delete()

                    return Response(
                        {"message": "Order created successfully"},
                        status=status.HTTP_201_CREATED,
                    )
            else:
                return Response(
                    {"message": "Unauthorized to create order"},
                    status=status.HTTP_403_FORBIDDEN,
                )
    else:
        return Response(
            {"message": "Anonymous user, login first"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET", "POST", "DELETE", "PUT", "PATCH"])
def single_order(request, id):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                order = Order.objects.get(pk=id)
                # Check if the order's user_id matches the current authenticated user's ID
                if order.user_id == request.user.id:
                    # The current authenticated user made this order
                    serialized_item = OrderSerializer(order)
                    return Response(serialized_item.data)
                else:
                    # The current authenticated user did not make this order
                    return Response(
                        {"message": "This order does not belong to the current user"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except Order.DoesNotExist:
                return Response(
                    {"message": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        if request.method == "DELETE":
            if request.user.groups.filter(name="Manager").exists():
                item = get_object_or_404(Order, pk=id)
                item.delete()
                return Response({"message": "Order deleted"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "You're not allowed to perform this action"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        if request.method == "PUT":
            if request.user.groups.filter(name="Manager").exists():
                item = get_object_or_404(Order, pk=id)
                serializer = OrderSerializer(item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message": "You're not allowed to perform this action"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        if request.method == "PATCH":
            try:
                order = Order.objects.get(pk=id)

                if request.user.groups.filter(name="Manager").exists():
                    # Allow Manager to change the order status
                    serializer = OrderSerializer(order, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                elif request.user.groups.filter(name="Delivery crew").exists():
                    # Allow Delivery crew to change the order status only
                    serializer = OrderSerializer(
                        order, data=request.data, partial={"status"}
                    )
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                else:
                    return Response(
                        {"message": "Unauthorized to perform this action"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

            except Order.DoesNotExist:
                return Response(
                    {"message": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

    else:
        return Response(
            {"message": "Anonymous user, login first"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
