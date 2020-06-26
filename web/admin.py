from django.contrib import admin

from .models import *

admin.site.register(Product)
admin.site.register(Pay)


class CartEntryInline(admin.TabularInline):
    model = CartEntry
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartEntryInline
    ]
