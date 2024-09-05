from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'last_login', 'date_joined']


class MenuItemSerializer(serializers.ModelSerializer):
    menuitem_id = serializers.IntegerField(read_only=True)
    category = serializers.CharField()

    class Meta:
        model = MenuItem
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        category_identifier = validated_data.pop('category')
        # Check if the category identifier is a digit (which might indicate a PK)
        if category_identifier.isdigit():
            try:
                category = Category.objects.get(pk=category_identifier)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    f"Category with ID '{category_identifier}' does not exist.")
        else:
            try:
                category = Category.objects.get(title=category_identifier)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    f"Category '{category_identifier}' does not exist.")

        menu_item = MenuItem.objects.create(
            category=category, **validated_data)
        return menu_item

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category_identifier = validated_data.pop('category')
            # Check if the category identifier is a digit (which might indicate a PK)
            if category_identifier.isdigit():
                try:
                    category = Category.objects.get(pk=category_identifier)
                except Category.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Category with ID '{category_identifier}' does not exist.")
            else:
                try:
                    category = Category.objects.get(title=category_identifier)
                except Category.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Category '{category_identifier}' does not exist.")

        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menu_item', 'quantity', 'unit_price']
        depth = 1

    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            instance.user = instance.user
            instance.menu_item = instance.menu_item
            instance.quantity = validated_data.get(
                'quantity', instance.quantity)
            instance.unit_price = instance.unit_price
            instance.save()
            return instance
        else:
            return Response({"message": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menu_item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'
