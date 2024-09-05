from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import Http404

from ..models import MenuItem, Cart, User
from ..serializers import MenuItemSerializer, UserSerializer, CartSerializer


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.filter(carts__user=request.user)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user = request.user
        menu_items = MenuItem.objects.filter(carts__user=user)
        if menu_items.filter(name=request.data['menuitem']).exists():
            return Response({"message": "Item already in cart"}, status=status.HTTP_400_BAD_REQUEST)
        menuitem = get_object_or_404(MenuItem, name=request.data['menuitem'])
        quantity = request.data['quantity']
        unit_price = menuitem.price
        cart = Cart.objects.create(
            user=user, menu_item=menuitem, quantity=quantity, unit_price=unit_price)
        return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)
    else:
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request, pk):
    if request.method == 'PATCH':
        try:
            cart = get_object_or_404(Cart, pk=pk)
        except Http404:
            return Response({"message": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != cart.user:
            return Response({"message": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
    else:
        try:
            cart = get_object_or_404(Cart, pk=pk)
        except Http404:
            return Response({"message": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != cart.user:
            return Response({"message": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        cart.delete()
        return Response({"message": "Cart deleted successfully"}, status=status.HTTP_200_OK)
