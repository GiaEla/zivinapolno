from django.contrib import admin

from pro.models import Product, Offer, Invoice, Reference, BankAccount, ProductQuantity, Vat, Activity, Event, \
    Event_detail, Discount


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('price_with_vat',)


class ProductQuantityInline(admin.StackedInline):
    model = ProductQuantity


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ProductQuantityInline]
    readonly_fields = ('invoice_number',)


class OfferAdmin(admin.ModelAdmin):
    readonly_fields = ('offer_number',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Offer)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Reference)
admin.site.register(BankAccount)
admin.site.register(ProductQuantity)
admin.site.register(Vat)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(Event_detail)
admin.site.register(Discount)
