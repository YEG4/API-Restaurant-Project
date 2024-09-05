from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import requests
"""This file contains views for registration endpoints.
"""


@api_view(['POST'])
def register(request):
    """This api endpoint is used to register a user

    Args:
        request (HttpRequest object): The request object

    Returns:
        JSON: A JSON response containing the user's tokens
    """
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'message': 'Username and Password are required'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    register_url = request.build_absolute_uri('/auth/users/')
    create_token_url = request.build_absolute_uri('/auth/jwt/create/')
    payload = {'username': username, 'password': password}
    user_info = requests.post(register_url, data=payload).json()
    tokens = requests.post(create_token_url, data=payload).json()

    return Response({"tokens": tokens}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_tokens(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'message': 'Username and Password are required'}, status=status.HTTP_400_BAD_REQUEST)
    create_token_url = request.build_absolute_uri('/auth/jwt/create/')
    payload = {'username': username, 'password': password}
    tokens = requests.post(create_token_url, data=payload).json()

    return Response({"tokens": tokens}, status=status.HTTP_201_CREATED)
