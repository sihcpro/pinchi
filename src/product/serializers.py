from rest_framework import serializers

from .models import Product, Category, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "_created", "_updated"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "department", "_created", "_updated"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["department"] = DepartmentSerializer(instance.department).data
        return data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "category", "_created", "_updated"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = CategorySerializer(instance.category).data
        return data
