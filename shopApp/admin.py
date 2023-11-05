from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Shoes, Tshirt, Trouser, Image, Brand


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "main_photo", "image", "thumbnail"]
    prepopulated_fields = {"slug": ("name",)}


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ["name", "main_photo", "image", "display_thumbnail"]

    readonly_fields = ["display_thumbnail"]

    def display_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" />'.format(obj.image.url)
            )
        return ""

    display_thumbnail.short_description = "Thumbnail"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["price", "available"]
    inlines = [ImageInline]


@admin.register(Tshirt)
class TshirtAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["price", "available"]
    inlines = [ImageInline]


@admin.register(Trouser)
class TrouserAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["price", "available"]
    inlines = [ImageInline]
