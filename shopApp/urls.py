from django.urls import path, include
from .views import ProductViewSet, CategoryListView, BrandListView, ImageListView

app_name = "shop"

urlpatterns = [
    path(
        "products/",
        ProductViewSet.as_view(
            {
                "get": "list",
                "post": "create"
            }
        ),
        name="products_list",
    ),
    path(
        "products/<slug:category_slug>/",
        ProductViewSet.as_view({"get": "list"}),
        name="products_list_by_category",
    ),
    path(
        "products/<int:pk>/<slug:slug>/",
        ProductViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="product_detail",
    ),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("brands/", BrandListView.as_view(), name="brand_list"),
    path("images/", ImageListView.as_view(), name="image_list"),
]
