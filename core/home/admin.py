from django.contrib import admin
from .models import *
# Register your models here.



admin.site.register(Categorie)
admin.site.register(Product)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['product', 'start_time', 'end_time', 'created_by']
    fields = ['product', 'start_time', 'end_time']

    def save_model(self, request, obj, form, change):
        # Set created_by to the current admin user
        obj.created_by = request.user
        super().save_model(request, obj, form, change)