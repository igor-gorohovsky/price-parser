from django.contrib import admin
from .models import Urls, Prices


class UrlsAdmin(admin.ModelAdmin):
    list_display = ('id', 'url')
    list_display_links = ('id', 'url')


class PricesAdmin(admin.ModelAdmin):
    list_display = ('url_id', 'date', 'current_price', 'status')
    search_fields = ('current_price', 'status')
    list_filter = ('status',)


admin.site.register(Urls, UrlsAdmin)
admin.site.register(Prices, PricesAdmin)
