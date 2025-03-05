from django.contrib import admin
from .models import *

admin.site.site_header = "MayTinhVui"
admin.site.site_title = "MayTinhVui Admin"
admin.site.index_title = "Quản lý cửa hàng MayTinhVui"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_discounted_price', 'quantity', 'category', 'manufacturer')
    list_filter = ('category', 'manufacturer', 'create')
    search_fields = ('name',)
    ordering = ('-create',)
    list_editable = ('price', 'quantity')
    readonly_fields = ('get_discounted_price',)
    fieldsets = (
        ('Thông tin sản phẩm', {
            'fields': ('name', 'category', 'manufacturer', 'price', 'quantity', 'detail')
        }),
        ('Hình ảnh sản phẩm', {
            'fields': ('image',)
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update')
    search_fields = ('name',)

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update')
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating',)

class CheckoutInfoAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'number', 'city', 'district', 'town', 'hamlet')
    search_fields = ('order__id', 'name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'purchase_date')
    search_fields = ('customer__username', 'id')

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'quantity')

class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount', 'start', 'end')
    list_filter = ('start', 'end')

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(CheckoutInfo, CheckoutInfoAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Offer, OfferAdmin)
