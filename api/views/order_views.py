from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Sum

from ..models import MenuItem, Cart, User, Order, OrderItem
from ..serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderItemSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    user = request.user
    is_manager = user.groups.filter(name='Manager').exists()
    is_delivery_crew = user.groups.filter(name='Delivery crew').exists()
    if request.method == 'GET':
        if is_manager:
            orderitems = OrderItem.objects.all()
            serializer = OrderItemSerializer(orderitems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_delivery_crew:
            orders = OrderItem.objects.filter(order__delivery_crew=user)
            serializer = OrderItemSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        orderitems = OrderItem.objects.filter(user=user)
        if not orderitems:
            return Response({"message": "No orders found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(orderitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            carts = Cart.objects.filter(user=user)
        except Http404:
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        total_price = sum([cart.get_total for cart in carts])
        order = Order.objects.create(user=user, total=total_price)
        for cart in carts:
            OrderItem.objects.create(user=user,
                                     order=order, menu_item=cart.menu_item, quantity=cart.quantity, unit_price=cart.unit_price)
        # carts.delete()
        return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def display_order(request, orderId):
    user = request.user
    is_manager = request.user.groups.filter(name="Manager").exists()
    is_delivery_crew = request.user.groups.filter(
        name="Delivery crew").exists()
    if request.method == "GET":
        if (not is_manager) and (not user.is_superuser) and (not is_delivery_crew):
            order_obj = OrderItem.objects.filter(order_id=orderId)
            if order_obj:
                if order_obj[0].order.user.username == request.user.username:
                    serializer = OrderItemSerializer(order_obj, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Order not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                return Response(
                    {"message": "Order Not Found."}, status=status.HTTP_404_NOT_FOUND
                )

    if request.method == "PATCH":
        if is_delivery_crew:
            order_obj = OrderItem.objects.filter(order_id=orderId).exists()
            if order_obj:
                order = get_object_or_404(Order, id=orderId)
                order.status = request.POST["status"]
                order.save()
                return Response(order.status, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Order Not Found."}, status=status.HTTP_404_NOT_FOUND
                )
        if (not is_manager) and (not user.is_superuser) and (not is_delivery_crew):
            order_item = get_object_or_404(OrderItem, id=orderId)
            if order_item:
                if order_item.order.user.username == request.user.username:
                    serializer = OrderItemSerializer(
                        order_item, data=request.POST, partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"message": "Access denied."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"message": "Order Not Found."}, status=status.HTTP_404_NOT_FOUND
                )
    if request.method == "DELETE":
        if is_manager:
            order_items = OrderItem.objects.filter(order_id=orderId).delete()
            order = Order.objects.filter(id=orderId).delete()

            return Response(
                {"message": "Order has been deleted."}, status=status.HTTP_200_OK
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assign_delivery_crew_to_order(request, orderId, userId):
    user = User.objects.filter(id=userId)
    if not user.groups.filter(name='Delivery crew').exists():
        return Response({"message": "User is not a delivery crew"}, status=status.HTTP_400_BAD_REQUEST)
    is_manager = user.groups.filter(name='Manager').exists()
    if not is_manager:
        return Response({"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN)
    order = Order.objects.filter(id=orderId)
    if not order:
        return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    order = order.first()
    order.delivery_crew = user
    order.save()
    return Response({"message": "Delivery crew assigned successfully"}, status=status.HTTP_200_OK)
