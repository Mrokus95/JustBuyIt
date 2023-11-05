from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils.deconstruct import deconstructible
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

MEN = "Men"
WOMAN = "Woman"
UNISEX = "Unisex"
SIZE_XS = "XS"
SIZE_S = "S"
SIZE_M = "M"
SIZE_L = "L"
SIZE_XL = "XL"
SIZE_XXL = "XXL"

GENDER_CHOICES = ((MEN, "Men"), (WOMAN, "Woman"), (UNISEX, "Unisex"))

SIZE_CHOICES = (
    (SIZE_XS, "XS"),
    (SIZE_S, "S"),
    (SIZE_M, "M"),
    (SIZE_L, "L"),
    (SIZE_XL, "XL"),
    (SIZE_XXL, "XXL"),
)


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:products_list_by_category", args=[self.slug])


class Product(PolymorphicModel):
    category = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.ForeignKey(
        Brand, related_name="brand_products", on_delete=models.CASCADE
    )
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "name"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])


@deconstructible
class ImagePath(object):
    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, instance, filename):
        return f'media/images/products/{instance.product.name}/{"main_photo" if instance.main_photo else "photos"}/{filename}'


class Image(models.Model):
    product = models.ForeignKey(
        Product, related_name="photos", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    main_photo = models.BooleanField(default=False)
    image = models.ImageField(upload_to=ImagePath("image"), blank=True)
    thumbnail = models.ImageField(upload_to=ImagePath("thumbnail"), blank=True)

    def __str__(self):
        return self.name


class Shoes(Product):
    size = models.PositiveIntegerField(
        default=25, validators=[MinValueValidator(25), MaxValueValidator(50)]
    )
    material = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=MEN)

    class Meta(Product.Meta):
        verbose_name = "shoes"
        verbose_name_plural = "shoes"


class Tshirt(Product):
    size = models.CharField(max_length=6, choices=SIZE_CHOICES, default=SIZE_L)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=MEN)

    class Meta(Product.Meta):
        verbose_name = "t-shirt"
        verbose_name_plural = "t-shirts"


class Trouser(Product):
    width = models.PositiveIntegerField(
        default=25, validators=[MinValueValidator(25), MaxValueValidator(40)]
    )
    length = models.PositiveIntegerField(
        default=25, validators=[MinValueValidator(25), MaxValueValidator(40)]
    )
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=MEN)

    class Meta(Product.Meta):
        verbose_name = "trouser"
        verbose_name_plural = "Trousers"
