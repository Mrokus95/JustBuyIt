from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductListView(ListView):
    template_name = "shop/product/list.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = None
        self.categories = Category.objects.all()
        self.products = Product.objects.filter(available=True)
        slug = self.kwargs.get("category_slug")
        if slug:
            self.category = get_object_or_404(Category, slug=slug)
            self.products = self.products.filter(category=self.category)

        return self.products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["categories"] = self.categories
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "shop/product/detail.html"
