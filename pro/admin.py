import os
import zipfile
from unicodedata import decimal

from io import BytesIO
from django.contrib import admin
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from pro.models import *


def generate_selected_pdf(modeladmin, request, queryset):

    if len(queryset) > 1:
        zip_subdir = "Racuni_predracuni"
        zip_filename = "%s.zip" % zip_subdir

        # Open StringIO to grab in-memory ZIP contents
        s = BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for obj in queryset:
            obj.generate_pdf()
            if isinstance(obj, Offer):
                file_name = settings.STATICFILES_DIRS[0] + '\\pdfs\\offers\\' + str(obj.offer_number) + '.pdf'

            elif isinstance(obj, Invoice):
                file_name = settings.STATICFILES_DIRS[0] + '\\pdfs\\invoices\\' + str(obj.invoice_number) + '.pdf'

            fdir, fname = os.path.split(file_name)
            zip_path = os.path.join(zip_subdir, fname)

            # Add file, at correct path
            zf.write(file_name, zip_path)

            # Must close zip for all contents to be written
        zf.close()

        resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    elif len(queryset) == 1:
        obj = queryset[0]
        obj.generate_pdf()
        if isinstance(obj, Offer):
            file_name = settings.STATICFILES_DIRS[0] + '\\pdfs\\offers\\' + str(obj.offer_number) + '.pdf'

        elif isinstance(obj, Invoice):
            file_name = settings.STATICFILES_DIRS[0] + '\\pdfs\\invoices\\' + str(obj.invoice_number) + '.pdf'

        with open(file_name, 'rb') as file_obj:
            resp = HttpResponse(file_obj, content_type="application/pdf")
            resp['Content-Disposition'] = 'attachment; filename="racun.pdf'

    return resp

generate_pdf.short_description = "Izvozi kot .pdf"


def admin_mail(modeladmin, request, queryset):
    for obj in queryset:
        subject = ''
        message = ''
        pdf_path = ''

        if isinstance(obj, Offer):
            obj.generate_pdf()
            html_context = {
                'recipient': obj.recipient,
                'type': 'predračun',
                'date': obj.date.date()
            }
            subject = 'Predračun št.' + str(obj.offer_number)
            message = render_to_string('mail/pdf_offer_invoice.html', html_context)
            recipient_mail = obj.recipient.email
            pdf_path = settings.STATICFILES_DIRS[0] + '\\pdfs\\offers\\' + str(obj.offer_number) + '.pdf'

        elif isinstance(obj, Invoice):
            obj.generate_pdf()
            html_context = {
                'recipient': obj.offer.recipient,
                'type': 'račun',
                'date': obj.date
            }
            subject = 'Račun št.' + str(obj.invoice_number)
            message = render_to_string('mail/pdf_offer_invoice.html', html_context)
            recipient_mail = obj.offer.recipient.email
            pdf_path = settings.STATICFILES_DIRS[0] + '\\pdfs\\offers\\' + str(obj.invoice_number) + '.pdf'

        email = EmailMessage(
            subject,
            message,
            'giacotesting@gmail.com',
            [recipient_mail],
        )

        email.attach_file(pdf_path)
        email.content_subtype = 'html'
        email.send()

send_mail.short_description = "Pošlji email"


def is_payed(modeladmin, request, queryset):
    for obj in queryset:
        obj.payed = True
        obj.save()
is_payed.short_description = "Označi kot plačano"


class ProductForm(forms.ModelForm):
    VAT_CHOICES = (
        ((Decimal(str(22.0))), '22%'),
        ((Decimal(str(9.5))), '9,5%'),
        ((Decimal(str(0.0))), '0%'),
    )

    vat = forms.ChoiceField(choices=VAT_CHOICES)


class EventForm(forms.ModelForm):
    BTN_TYPE_CHOICES = (
        ('Kupi karto', 'Kupi karto'),
        ('Prijavi se', 'Prijavi se'),
        ('Prihaja kmalu', 'Prihaja kmalu'),
        ('Doniraj', 'Doniraj')
    )

    btn_type = forms.ChoiceField(choices=BTN_TYPE_CHOICES)


class DiscountInline(NestedStackedInline):
    model = Discount
    extra = 0
    fk_name = 'product_event'


class ProductEventAdmin(admin.ModelAdmin):
    pass


class ProductEventInline(NestedStackedInline):
    model = ProductEvent
    extra = 1
    fk_name = 'event_detail'
    inlines = [DiscountInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductEventInline, self).get_form(request, obj, **kwargs)
        form.base_fields['product'].queryset = Product.objects.filter(event_based=True)
        return form


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('price_with_vat',)
    list_display = ('name',)
    form = ProductForm


class ImageAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'img', 'name')
    readonly_fields = ('image_tag',)
    list_display = ('name', 'image_tag')


class DiscountAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(DiscountAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['product'].queryset = Product.objects.filter(event_based=False)
        return form

    list_display = ('product', 'value_display')


class ProductQuantityInline(admin.StackedInline):
    model = ProductQuantity
    extra = 0


class ProductQuantityAdmin(admin.ModelAdmin):
    fields = ['product', 'offer', 'qt_value']


class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('invoice_number', 'offer')
    list_display = ('invoice_number', 'offer')
    actions = [generate_selected_pdf, admin_mail]


class OfferAdmin(admin.ModelAdmin):
    inlines = [ProductQuantityInline]
    readonly_fields = ('offer_number', 'total_no_vat', 'total_with_vat', 'total_with_discount')
    list_display = ('offer_number', 'date', 'total_with_vat',)
    actions = [generate_selected_pdf, is_payed, admin_mail]



class EventDetailAdmin(admin.ModelAdmin):
    inlines = [ProductEventInline]
    list_display = ('id',)


class EventDetailInline(NestedStackedInline):
    model = EventDetail
    extra = 1
    fk_name = 'event'
    inlines = [ProductEventInline]


class EventAdmin(NestedModelAdmin):
    model = Event
    form = EventForm
    inlines = [EventDetailInline]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email',)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'z_index')


class SubActivityAdmn(admin.ModelAdmin):
    list_display = ('name', 'z_index', 'activity')


admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Reference)
admin.site.register(BankAccount)
admin.site.register(ProductEvent, ProductEventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventDetail, EventDetailAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SubActivity, SubActivityAdmn)