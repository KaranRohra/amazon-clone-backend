from django.contrib import admin

from . import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 5


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category"]
    inlines = (ProductImageInline,)
    search_fields = ("name", )
    list_filter = ("category", )
