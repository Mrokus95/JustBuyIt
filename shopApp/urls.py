from django.urls import path, include
from .views import ProductListView, ProductDetailView

app_name = "shop"

urlpatterns = [
    path("", 
        ProductListView.as_view(), 
        name="products_list"
        ),
    path("<slug:category_slug>/",
        ProductListView.as_view(),
        name="products_list_by_category",
    ),
    path("<int:id>/<slug:slug>/", 
        ProductDetailView.as_view(), 
        name="product_detail"
        ),
]
