from rest_framework import serializers
from .models import Product, Category, Brand, Image
from django.utils.text import slugify

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class ProductImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "main_photo", "image", "thumbnail"]

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True, many=True)
    url = serializers.CharField(source="get_absolute_url", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images_queryset = Image.objects.filter(product=obj)
        images_serializer = ProductImageListSerializer(images_queryset, many=True)
        return images_serializer.data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "brand",
            "category",
            "url",
            "price",
            "available",
            "images",
        ]

class WriteProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "brand",
            "category",
            "price",
            "available",
            "images",
        ]

    def create(self, validated_data):
        images_data = validated_data.pop("images", None)
        categories_data = validated_data.pop("category", [])
        product = Product.objects.create(**validated_data)
        product.category.set(categories_data)

        if images_data:
            for image_data in images_data:
                Image.objects.create(product=product, image=image_data)

        return product
    
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.slug = slugify(validated_data['name'])

        super().update(instance, validated_data)

        return instance
    