from django.contrib import admin
from .models import *
# Register your models here.



admin.site.register(Categorie)
# admin.site.register(Product)
admin.site.register(Winner)

admin.site.register(ContectUs)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['product', 'start_time', 'end_time', 'created_by']
    fields = ['product', 'start_time', 'end_time']

    def save_model(self, request, obj, form, change):
        # Set created_by to the current admin user
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Set the created_by field to the currently logged-in user
        if not obj.created_by and request.user.is_authenticated:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)