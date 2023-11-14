from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category, Brand, Image
from rest_framework import generics, viewsets, permissions, status
from .serializers import CategoryListSerializer, ProductSerializer, WriteProductSerializer, BrandListSerializer, ImageListSerializer
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer

class ImageListView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageListSerializer
    
class ProductViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action in ['list', 'retrive']:
            return ReadProductSerializer
        return WriteProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        queryset = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product_slug = kwargs.get('slug')

        instance = get_object_or_404(Product, id=product_id, slug=product_slug)
        serializer = ProductSerializer(instance)
        return Response(serializer.data)
