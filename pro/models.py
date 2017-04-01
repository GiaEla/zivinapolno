from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from utils.generators import generate_object_number, generate_price_with_vat


class Profile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(_('Address'), max_length=50, blank=True, null=True)
    city = models.CharField(_('City'), max_length=40, blank=True, null=True)
    post = models.CharField(_('Last name'), max_length=40, blank=True, null=True)
    token = models.CharField(_('Token'), max_length=15, unique=True, db_index=True, null=True)
    subscribed = models.CharField(_('Subscribed or not'), max_length=2, blank=True, null=True)


class Vat(models.Model):
    value = models.DecimalField('DDV', max_digits=8, decimal_places=2)

    def __unicode__(self):
        return '%s' % self.value

    def __str__(self):
        return '%s' % self.value

    class Meta:
        verbose_name = _(u'stopnja DDV')
        verbose_name_plural = _(u'stopnje DDV')


class Product(models.Model):
    name = models.CharField('Izdelek', max_length=50)
    description = models.CharField('Opis', max_length=500)
    product_image = models.ImageField('Slika', null=True)
    price_no_vat = models.DecimalField('Cena brez DDV', max_digits=8, decimal_places=2)
    price_with_vat = models.DecimalField('Cena z DDV', max_digits=8, decimal_places=2)
    vat = models.ForeignKey(Vat, verbose_name='DDV')
    event_based = models.BooleanField('Produkt je vezan na dogodek', default=True)

    def __unicode__(self):
        return '%s : %s€' % (self.name, self.price_with_vat)

    def __str__(self):
        return '%s : %s€' % (self.name, self.price_with_vat)

    class Meta:
        verbose_name = _(u'izdelek')
        verbose_name_plural = _(u'izdelki')

    def save(self, *args, **kwargs):
        self.price_with_vat = generate_price_with_vat(self.price_no_vat, self.vat.value)

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


class Offer(models.Model):
    date = models.DateTimeField('Datum')
    place = models.CharField('Kraj', max_length=100)
    offer_number = models.PositiveIntegerField('Predračun', editable=False, null=False)
    products = models.ManyToManyField(Product, through='ProductQuantityOffer', verbose_name='Izdelki')
    total_no_vat = models.DecimalField('Znesek brez DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    total_with_vat = models.DecimalField('Znesek z DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    recipient = models.ForeignKey(User, verbose_name='Prejemnik')
    reference = models.ForeignKey('Reference', verbose_name='Referenca')
    bank_account = models.ForeignKey('BankAccount', verbose_name='Bančni račun')
    payed = models.BooleanField('Plačano', default=False)

    def __unicode__(self):
        return '%s %s' % self.offer_number, self.date

    def __str__(self):
        return '%s' % self.offer_number

    class Meta:
        verbose_name = _(u'predračun')
        verbose_name_plural = _(u'predračuni')

    def save(self, *args, **kwargs):
        # if new offer, it generates number, otherwise it's not overwritten
        if self.offer_number is None:
            last_object = Offer.objects.all().order_by('date').last()
            self.offer_number = generate_object_number(self.date, last_object, 'offer')

        super(Offer, self).save(*args, **kwargs)


class Invoice(models.Model):
    date = models.DateTimeField('Datum')
    place = models.CharField('Kraj', max_length=100)
    products = models.ManyToManyField(Product, through='ProductQuantityInvoice', verbose_name='Izdelki')
    total_no_vat = models.DecimalField('Znesek brez DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    total_with_vat = models.DecimalField('Znesek z DDV', max_digits=8, decimal_places=2, default=0, editable=False)
    invoice_number = models.PositiveIntegerField('Račun', editable=False, null=False)
    recipient = models.ForeignKey(User,verbose_name='Prejemnik')
    reference = models.ForeignKey('Reference', verbose_name='Referenca')
    bank_account = models.ForeignKey('BankAccount', verbose_name='Bančni račun')
    offer = models.ForeignKey('Offer', blank=True, null=True, verbose_name='Predračun')

    def __unicode__(self):
        return '%s' % self.invoice_number

    def __str__(self):
        return '%s' % self.invoice_number


    class Meta:
        verbose_name = _(u'račun')
        verbose_name_plural = _(u'računi')

    def save(self, *args, **kwargs):
        # if new invoice, it generates number, otherwise it's not overwritten
        if self.invoice_number is None:
            last_object = Invoice.objects.all().order_by('date').last()
            self.invoice_number = generate_object_number(self.date, last_object, 'invoice')

        super(Invoice, self).save(*args, **kwargs)


class InvoiceForm(ModelForm):

    class Meta:
        model = Invoice
        fields = ['date',
                  'place',
                  'products',
                  'recipient',
                  'reference',
                  'bank_account',
                  'offer']

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.fields['products'].required = True


class ProductQuantityInvoice(models.Model):
    product = models.ForeignKey(Product, default=1)
    invoice = models.ForeignKey(Invoice, default=1)
    qt_value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _(u'količina izdelka na računu')
        verbose_name_plural = _(u'količina izdelka na računu')

    def __unicode__(self):
        return '%s' % self.invoice.invoice_number

    def __str__(self):
        return '%s' % self.invoice.invoice_number

    def save(self, *args, **kwargs):

        price_no_vat_invoice = 0
        price_with_vat_invoice = 0

        product_quantities_invoice = ProductQuantityInvoice.objects.filter(invoice=self.invoice).exclude(id=self.id)

        for product_quantity_inv in product_quantities_invoice:
            price_with_vat_invoice += Decimal(str(product_quantity_inv.qt_value)) * product_quantity_inv.product.price_with_vat
            price_no_vat_invoice += Decimal(str(product_quantity_inv.qt_value)) * product_quantity_inv.product.price_no_vat

        # adds current product
        price_with_vat_invoice += Decimal(str(self.qt_value)) * self.product.price_with_vat
        price_no_vat_invoice += Decimal(str(self.qt_value)) * self.product.price_no_vat

        this_invoice = Invoice.objects.get(id=self.invoice.id)
        this_invoice.total_with_vat = price_with_vat_invoice
        this_invoice.total_no_vat = price_no_vat_invoice
        this_invoice.save()

        super(ProductQuantityInvoice, self).save(*args, **kwargs)


class ProductQuantityOffer(models.Model):
    product = models.ForeignKey(Product, default=1)
    offer = models.ForeignKey(Offer, default=1)
    qt_value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _(u'količina izdelka na predračunu')
        verbose_name_plural = _(u'količina izdelka na predračunu')

    def __unicode__(self):
        return '%s' % self.offer.offer_number

    def __str__(self):
        return '%s' % self.offer.offer_number

    def save(self, *args, **kwargs):
        price_no_vat_offer = 0
        price_with_vat_offer = 0

        product_quantities_offer = ProductQuantityOffer.objects.filter(offer=self.offer).exclude(id=self.id)

        for product_quantity_off in product_quantities_offer:
            price_with_vat_offer += Decimal(str(product_quantity_off.qt_value)) * product_quantity_off.product.price_with_vat
            price_no_vat_offer += Decimal(str(product_quantity_off.qt_value)) * product_quantity_off.product.price_no_vat

        # adds current product
        price_with_vat_offer += Decimal(str(self.qt_value)) * self.product.price_with_vat
        price_no_vat_offer += Decimal(str(self.qt_value)) * self.product.price_no_vat

        this_offer = Offer.objects.get(id=self.offer.id)
        this_offer.total_with_vat = price_with_vat_offer
        this_offer.total_no_vat = price_no_vat_offer
        this_offer.save()

        super(ProductQuantityOffer, self).save(*args, **kwargs)


class Activity(models.Model):
    name = models.CharField('Dejavnost', max_length=50)
    description = models.CharField('Opis', max_length=500)
    image = models.ImageField('Slika', null=True)

    class Meta:
        verbose_name = _(u'dejavnost zavoda')
        verbose_name_plural = _(u'dejavnost zavoda')


class Event(models.Model):
    name = models.CharField('Generalni dogodek', max_length=50)
    description = models.CharField('Opis', max_length=500)
    date_from = models.DateField('Pričetek', null=True)
    date_to = models.DateField('Zaključek', null=True)
    independently_sold = models.BooleanField('Možen je nakup posamičnih vstopnic', default=False)

    class Meta:
        verbose_name = _(u'generalni dogodek')
        verbose_name_plural = _(u'generalni dogodki')


class EventDetail(models.Model):
    name = models.CharField('Dogodek', max_length=50)
    event = models.ForeignKey(Event, default=1, verbose_name='Generalni dogodek')
    date_from = models.DateField('Datum pričetka', null=True)
    from_hour = models.TimeField('Ura pričetka', null=True)
    date_to = models.DateField('Zaključek', null=True)
    all_tickets = models.PositiveSmallIntegerField('Število vseh vstopnic', null=True)


    class Meta:
        verbose_name = _(u'Dogodek')
        verbose_name_plural = _(u'Dogodki')


class Discount(models.Model):

    name = models.CharField('Popust', max_length=50)
    date_from = models.DateField('Pričetek', null=True)
    date_to = models.DateField('Zaključek', null=True)
    from_quantity = models.PositiveSmallIntegerField('Količinski popust', null=True)
    value = models.DecimalField('Vrednost popusta', max_digits=8, decimal_places=2, null=False)

    class Meta:
        verbose_name = _(u'Popust')
        verbose_name_plural = _(u'Popusti')


class ProductEvent(models.Model):
    event_detail = models.ForeignKey(EventDetail, verbose_name='Dogodek')
    product = models.ForeignKey(Product, verbose_name='Izdelek')
    sold_tickets = models.SmallIntegerField('Število prodanih kart')

    class Meta:
        verbose_name = _(u'Izdelek, vezan na dogodek')
        verbose_name_plural = _(u'Izdelki, vezani na dogodek')


class ProductDiscount(models.Model):
    product = models.ForeignKey(Product, verbose_name='Izdelek')
    discount = models.ForeignKey(Discount, verbose_name='Popust')

    verbose_name = _(u'Popust za izdelke')
    verbose_name_plural = _(u'Popusti za izdelke')


class ProductEventDiscount(models.Model):
    product_event = models.ForeignKey(ProductEvent, verbose_name='Izdelek, vezan na dogodek')
    discount = models.ForeignKey(Discount, verbose_name='Popust')

    class Meta:
        verbose_name = _(u'Popust za izdelke, vezane na dogodek')
        verbose_name_plural = _(u'Popusti za izdelke, vezane na dogodek')
