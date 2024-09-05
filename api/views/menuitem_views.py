from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, throttle_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404

from ..serializers import *


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_menu_items(request):
    """This api endpoint is used to get all menu items

    Args:
        request (HttpRequest object): The request object

    Returns:
        JSON: A JSON response containing all menu items
    """
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    else:
        if request.user.groups.filter(name='Manager').exists():
            serializer = MenuItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Menu Item created successfully"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You do not have permission to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_menu_item(request, id):
    """This api endpoint is used to get a single menu item

    Args:
        request (HttpRequest object): The request object

    Returns:
        JSON: A JSON response containing menu item
    """
    if request.method == 'GET':
        menu_item = get_object_or_404(MenuItem, id=id)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.user.groups.filter(name='Manager').exists():
            menu_item = get_object_or_404(MenuItem, id=id)
            serializer = MenuItemSerializer(
                menu_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Menu Item updated successfully", "menu_item": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "You do not have permission to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            menu_item = get_object_or_404(MenuItem, id=id)
            menu_item.delete()
            return Response({"message": "Menu Item deleted successfully"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "You do not have permission to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
