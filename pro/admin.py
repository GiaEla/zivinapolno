from django.contrib import admin

from pro.models import *


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('price_with_vat',)


class ProductQuantityInvoiceInline(admin.StackedInline):
    model = ProductQuantityInvoice
    extra = 0


class ProductQuantityInvoiceAdmin(admin.ModelAdmin):
    fields = ['product', 'invoice', 'qt_value']


class ProductQuantityOfferInline(admin.StackedInline):
    model = ProductQuantityOffer
    extra = 0


class ProductQuantityOfferAdmin(admin.ModelAdmin):
    fields = ['product', 'offer', 'qt_value']


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ProductQuantityInvoiceInline]
    readonly_fields = ('invoice_number', 'total_no_vat', 'total_with_vat')
    list_display = ('invoice_number', 'date', 'total_with_vat',)


class OfferAdmin(admin.ModelAdmin):
    inlines = [ProductQuantityOfferInline]
    readonly_fields = ('offer_number', 'total_no_vat', 'total_with_vat')
    list_display = ('offer_number', 'date', 'total_with_vat',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Reference)
admin.site.register(BankAccount)
# admin.site.register(ProductQuantity)
admin.site.register(Vat)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(EventDetail)
admin.site.register(Discount)
