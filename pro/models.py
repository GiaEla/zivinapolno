from datetime import timedelta, datetime
from decimal import Decimal
from django.contrib.auth.models import User, AbstractUser
from decimal import Decimal, ROUND_HALF_EVEN, Context

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, request
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from utils.generators import generate_object_number, generate_price_with_vat, generate_pdf




class UserProfile(AbstractUser):
    address = models.CharField(_('Naslov'), max_length=50, blank=True, null=True)
    city = models.CharField(_('Kraj'), max_length=40, blank=True, null=True)
    post = models.CharField(_('Poštna številka'), max_length=40, blank=True, null=True)
    token = models.CharField(_('Token'), max_length=15, unique=True, db_index=True, null=True)
    subscribed = models.CharField(_('Obveščanje'), max_length=2, blank=True, null=True)


class Image(models.Model):
    img = models.ImageField(upload_to="media")
    name = models.CharField('Ime', max_length=20, null=True)

    def image_tag(self):
        return mark_safe('<img src="{0}" style="width:auto; height:200px;" />'.format(settings.BASE_URL + str(self.img)))

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = _(u'slika')
        verbose_name_plural = _(u'slike')

    def __unicode__(self):
       # return mark_safe('<img src="{0}" style="width:auto; height:30px;" />'.format(settings.BASE_URL + str(self.img)))
        return '%s' % self.name

    def __str__(self):
        # return mark_safe('<img src="{0}" style="width:auto; height:30px;" />'.format(settings.BASE_URL + str(self.img)))
        return '%s' % self.name


class Product(models.Model):
    name = models.CharField('Izdelek', max_length=50)
    description = models.CharField('Opis', max_length=500)
    product_image = models.ImageField('Slika', null=True, blank=True)
    price_no_vat = models.DecimalField('Cena brez DDV', max_digits=8, decimal_places=2)
    price_with_vat = models.DecimalField('Cena z DDV', max_digits=8, decimal_places=2)
    vat = models.DecimalField('Cena z DDV', max_digits=8, decimal_places=1)
    event_based = models.BooleanField('Produkt je vezan na dogodek', default=True)

    def __unicode__(self):
        return '%s : %s€' % (self.name, self.price_with_vat)

    def __str__(self):
        return '%s : %s€' % (self.name, self.price_with_vat)

    class Meta:
        verbose_name = _(u'izdelek')
        verbose_name_plural = _(u'izdelki')

    def save(self, *args, **kwargs):
        self.price_with_vat = generate_price_with_vat(self.price_no_vat, self.vat)

        super(Product, self).save(*args, **kwargs)


class Reference(models.Model):
    name = models.CharField('Ime', max_length=50)
    reference = models.PositiveSmallIntegerField('Referenca')

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _(u'bančna referenca')
        verbose_name_plural = _(u'bančne reference')


class BankAccount(models.Model):
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=30, null=False)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _(u'bančni račun')
        verbose_name_plural = _(u'bančni računi')


class Event(models.Model):
    name = models.CharField('Generalni dogodek', max_length=50)
    short_description = models.CharField('kratek opis', max_length=30, null=True)
    description = models.CharField('Opis', max_length=500)
    date_from = models.DateField('Pričetek', null=True)
    date_to = models.DateField('Zaključek', null=True)
    independently_sold = models.BooleanField('Možen je nakup posamičnih vstopnic', default=False)
    img_event = models.ForeignKey(Image, verbose_name='slika', null=True)
    btn_type = models.CharField('Napis na gumbu', max_length=50, default=None)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _(u'ustvari dogodek')
        verbose_name_plural = _(u'ustvari dogodek')


class EventDetail(models.Model):
    name = models.CharField('Dogodek', max_length=50)
    event = models.ForeignKey(Event, default=1, verbose_name='Generalni dogodek')
    date_from = models.DateField('Datum pričetka', null=True)
    from_hour = models.TimeField('Ura pričetka', null=True)
    date_to = models.DateField('Zaključek', null=True)
    all_tickets = models.PositiveSmallIntegerField('Število vseh vstopnic', null=True)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _(u'Dogodek')
        verbose_name_plural = _(u'Dogodki')


class ProductEvent(models.Model):
    event_detail = models.ForeignKey(EventDetail, verbose_name='Dogodek')
    product = models.ForeignKey(Product, verbose_name='Izdelek')
    sold_tickets = models.SmallIntegerField('Število prodanih kart', default=0)

    class Meta:
        verbose_name = _(u'Izdelek, vezan na dogodek')
        verbose_name_plural = _(u'Izdelki, vezani na dogodek')

    def __unicode__(self):
        return '%s: %s' % (self.product.name, self.event_detail)

    def __str__(self):
        return '%s: %s' % (self.product.name, self.event_detail)


class Discount(models.Model):
    date_from = models.DateField('Pričetek', null=True)
    date_to = models.DateField('Zaključek', null=True)
    from_quantity = models.PositiveSmallIntegerField('Količinski popust', default=0)
    value = models.DecimalField('Vrednost popusta', max_digits=8, decimal_places=2, null=True, blank=True)
    product = models.ForeignKey(Product, blank=True, null=True, default=0, verbose_name='izdelek')
    product_event = models.ForeignKey(ProductEvent, blank=True, null=True, default=0, verbose_name='izdelek, vezan na dogodek')

    class Meta:
        verbose_name = _(u'Popust')
        verbose_name_plural = _(u'Popusti')

    def __unicode__(self):
        return '%s: %s' % (self.product.name, self.value)

    def __str__(self):
        return '%s: %s' % (self.product.name, self.value)

    def value_display(self):
        return '{0}%'.format(self.value)
    value_display.short_description = 'value'


class Offer(models.Model):
    date = models.DateTimeField('Datum')
    place = models.CharField('Kraj', max_length=100)
    offer_number = models.PositiveIntegerField('Predračun', editable=False, null=False)
    products = models.ManyToManyField(Product, through='ProductQuantity', verbose_name='Izdelki')
    total_no_vat = models.DecimalField('Znesek brez DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    total_with_vat = models.DecimalField('Znesek z DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    total_with_discount = models.DecimalField('Znesek s popustom', max_digits=8, decimal_places=2, default=0, editable=False)
    recipient = models.ForeignKey(UserProfile, verbose_name='Prejemnik')
    reference = models.ForeignKey('Reference', verbose_name='Referenca')
    bank_account = models.ForeignKey('BankAccount', verbose_name='Bančni račun')
    payed = models.BooleanField('Plačano', default=False)
    pay_until = models.DateField('Rok plačila', null=True, editable=False)

    def __unicode__(self):
        return '%s %s' % (self.offer_number, self.date)

    def __str__(self):
        return '%s' % self.offer_number

    # def download_pdf(self):
    #     selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    #     for select in selected:
    #         OfferWrapper.generate_offer(select)

    class Meta:
        verbose_name = _(u'predračun')
        verbose_name_plural = _(u'predračuni')

    def calculate_prices(self):

        products_quantities = ProductQuantity.objects.filter(offer=self)
        product_with_prices = []
        discount = Decimal(str('0.00'))
        self.total_no_vat = Decimal(str('0.00'))
        self.total_with_vat = Decimal(str('0.00'))
        self.total_with_discount = Decimal(str('0.00'))
        price_no_vat = Decimal(str('0.00'))
        price_with_vat = Decimal(str('0.00'))
        price_with_discount = Decimal(str('0.00'))

        for quantity in products_quantities:

            if quantity.product is not None:
                discounts = Discount.objects.filter(
                    date_from__lte=self.date,
                    date_to__gte=self.date,
                    from_quantity__lte=quantity.qt_value,
                    product=quantity.product
                ).order_by('-value')

                if len(discounts) > 0:
                    discount = discounts[0].value

                price_no_vat = quantity.product.price_no_vat * quantity.qt_value
                price_with_vat = quantity.product.price_with_vat * quantity.qt_value
                price_with_discount = price_with_vat - (price_with_vat * (Decimal(str(discount / 100))))

                product_with_prices.append({
                    'name': quantity.product.name,
                    'quantity': quantity.qt_value,
                    'price_no_vat': price_no_vat,
                    'vat': quantity.product.vat,
                    'price_with_vat': price_with_vat,
                    'discount': discount,
                    'price_with_discount': price_with_discount,
                })

            elif quantity.product_event is not None:
                discounts = Discount.objects.filter(
                    date_from__lte=self.date,
                    date_to__gte=self.date,
                    from_quantity__lte=quantity.qt_value,
                    product_event=quantity.product_event
                ).order_by('-value')

                if len(discounts) > 0:
                    discount = discounts[0].value

                price_no_vat = quantity.product_event.product.price_no_vat * quantity.qt_value
                price_with_vat = quantity.product_event.product.price_with_vat * quantity.qt_value
                price_with_discount = price_with_vat - (price_with_vat * (Decimal(str(discount / 100))))

                product_with_prices.append({
                    'name': quantity.product_event.product.name,
                    'quantity': quantity.qt_value,
                    'price_no_vat': price_no_vat,
                    'vat': quantity.product_event.product.vat,
                    'price_with_vat': price_with_vat,
                    'discount': discount,
                    'price_with_discount': price_with_discount,
                })

            self.total_no_vat += price_no_vat
            self.total_with_vat += price_with_vat
            self.total_with_discount += price_with_discount

            self.total_no_vat.quantize(Decimal(1.00), rounding=ROUND_HALF_EVEN)
            self.total_with_vat.quantize(Decimal(1.00), rounding=ROUND_HALF_EVEN)
            self.total_with_discount.quantize(Decimal(1.00), rounding=ROUND_HALF_EVEN)

        super(Offer, self).save()

        return product_with_prices

    def generate_pdf(self):

        html_context = {
            'products': self.calculate_prices(),
            'offer_number': self.offer_number,
            'total_no_vat': self.total_no_vat,  # calculated in ProductQuantity save method
            'total_with_vat': self.total_with_vat,
            'total_with_discount': self.total_with_discount,
            'place': self.place,
            'date': self.date,
            'bank_account': self.bank_account.account,
            'reference': self.reference.reference,
            'pay_until': self.pay_until,
        }

        pdf_path = generate_pdf('offer.html', html_context, 'offers', str(self.offer_number) + '.pdf')

        return pdf_path

    def save(self, *args, **kwargs):
        # if new offer, it generates number, otherwise it's not overwritten
        if self.offer_number is None:
            last_object = Offer.objects.all().order_by('date').last()
            self.offer_number = generate_object_number(self.date, last_object, 'offer')

        # gives a week to pay the offer
        pay_in = timedelta(days=7)
        pay_until = self.date + pay_in
        self.pay_until = pay_until

        # if offer is paid, it generates invoice
        if self.payed is True:
            invoice = Invoice.objects.create()
            invoice.offer = self
            invoice.save()

        super(Offer, self).save(*args, **kwargs)


class Invoice(models.Model):
    date = models.DateField('Datum')
    invoice_number = models.PositiveIntegerField('Račun', editable=False, null=False)
    offer = models.ForeignKey('Offer', blank=True, null=True, verbose_name='Predračun')

    def __unicode__(self):
        return '%s' % self.invoice_number

    def __str__(self):
        return '%s' % self.invoice_number

    def generate_pdf(self):

        offer = self.offer

        html_context = {
            'products': offer.calculate_prices(),
            'invoice_number': self.invoice_number,
            'place': offer.place,
            'date': self.date,
            'total_no_vat': offer.total_no_vat,
            'total_with_vat': offer.total_with_vat,
            'total_with_discount': round(offer.total_with_discount, 2)
        }

        pdf_path = generate_pdf('invoice.html', html_context, 'invoices', str(self.invoice_number) + '.pdf')

        return pdf_path

    class Meta:
        verbose_name = _(u'račun')
        verbose_name_plural = _(u'računi')

    def save(self, *args, **kwargs):

        # if new invoice, it generates number, otherwise it's not overwritten
        self.date = datetime.now().date()
        if self.invoice_number is None:
            last_object = Invoice.objects.all().order_by('date').last()
            self.invoice_number = generate_object_number(self.date, last_object, 'invoice')

        super(Invoice, self).save(*args, **kwargs)


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, default=0, blank=True, null=True)
    product_event = models.ForeignKey(ProductEvent, default=0, blank=True,  null=True)
    offer = models.ForeignKey(Offer)
    qt_value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _(u'količina izdelka')
        verbose_name_plural = _(u'količine izdelkov')

    def __unicode__(self):
        return '%s' % self.offer.offer_number

    def __str__(self):
        return '%s' % self.offer.offer_number

    def save(self, *args, **kwargs):

        self.offer.calculate_prices()
        self.offer.save()

        super(ProductQuantity, self).save(*args, **kwargs)


class Activity(models.Model):
    name = models.CharField('Dejavnost', max_length=50)
    description = models.CharField('Opis', max_length=500)
    image = models.ImageField('Slika', null=True)

    class Meta:
        verbose_name = _(u'dejavnost zavoda')
        verbose_name_plural = _(u'dejavnost zavoda')

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name


