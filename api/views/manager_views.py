from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group

from ..serializers import UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_managers(request):
    """This api endpoint is used to get all managers

    Args:
        request (HttpRequest object): The request object

    Returns:
        JSON: A JSON response containing all managers
    """
    if request.method == 'GET':
        managers = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = get_object_or_404(User, username=username)
        except Http404:
            return Response({"message": "User does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response({"message": "User added to managers group successfully"},
                        status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def get_manager(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
    except Http404:
        return Response({"message": "User does not exist"},
                        status=status.HTTP_404_NOT_FOUND)
    managers = Group.objects.get(name='Manager')
    if user.groups.filter(name='Manager').exists():
        managers.user_set.remove(user)
        return Response({"message": "User removed from managers group successfully"},
                        status=status.HTTP_200_OK)
    else:
        return Response({"message": "User is not a manager"},
                        status=status.HTTP_400_BAD_REQUEST)
