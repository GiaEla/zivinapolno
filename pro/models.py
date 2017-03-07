from django.contrib.auth.models import User
from django.db import models
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
    vat = models.DecimalField('vat', max_digits=8, decimal_places=2)

    def __unicode__(self):
        return '%s' % self.vat

    def __str__(self):
        return '%s' % self.vat


class Product(models.Model):
    name = models.CharField('Name', max_length=50, null=False)
    description = models.CharField('Description', max_length=500, null=False)
    # product_image = models.ImageField('Name')
    price_no_vat = models.DecimalField('Price', max_digits=8, decimal_places=2, null=False)
    price_with_vat = models.DecimalField('Price with VAT', max_digits=8, decimal_places=2)
    vat = models.ForeignKey(Vat)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.price_with_vat = generate_price_with_vat(self.price_no_vat, self.vat)

        super(Product, self).save(*args, **kwargs)


class Offer(models.Model):
    date = models.DateTimeField(null=False)
    place = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='ProductQuantity')
    total_no_vat = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    total_with_vat = models.DecimalField(max_digits=8, decimal_places=2)
    offer_number = models.PositiveIntegerField(editable=False, unique=True, null=False)
    recipient = models.ForeignKey(User)
    reference = models.ForeignKey('Reference')
    bank_account = models.ForeignKey('BankAccount')

    def __unicode__(self):
        return '%s %s' % self.offer_number, self.date

    def __str__(self):
        return '%s' % self.offer_number

    def save(self, *args, **kwargs):
        # if new offer, it generates number, otherwise it's not overwritten
        if self.offer_number is None:
            last_object = Offer.objects.all().order_by('date').last()
            self.offer_number = generate_object_number(self.date, last_object, 'offer')

        super(Offer, self).save(*args, **kwargs)


class Invoice(models.Model):
    date = models.DateTimeField(null=False)
    place = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='ProductQuantity')
    total_no_vat = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    total_with_vat = models.DecimalField(max_digits=8, decimal_places=2)
    invoice_number = models.PositiveIntegerField(editable=False, null=False)
    recipient = models.ForeignKey(User)
    reference = models.ForeignKey('Reference')
    bank_account = models.ForeignKey('BankAccount')
    offer = models.ForeignKey('Offer')

    def __unicode__(self):
        return '%s' % self.invoice_number

    def __str__(self):
        return '%s' % self.invoice_number

    def save(self, *args, **kwargs):
        # if new invoice, it generates number, otherwise it's not overwritten
        if self.invoice_number is None:
            last_object = Invoice.objects.all().order_by('date').last()
            self.invoice_number = generate_object_number(self.date, last_object, 'invoice')

        super(Invoice, self).save(*args, **kwargs)


class Reference(models.Model):
    name = models.CharField(max_length=50)
    reference = models.PositiveSmallIntegerField(null=False)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name


class BankAccount(models.Model):
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=30, null=False)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return '%s' % self.name


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product)
    offer = models.ForeignKey(Offer)
    invoice = models.ForeignKey(Invoice)
    quantity = models.PositiveSmallIntegerField


class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    # image = models.ImageField('Activity_image')


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    date_from = models.DateField
    date_to = models.DateField
    product = models.ForeignKey(Product)


class EventDetail(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event)
    date_from = models.DateField
    date_to = models.DateField
    all_tickets = models.PositiveSmallIntegerField
    sold_tickets = models.PositiveSmallIntegerField


class Discount(models.Model):
    event_key = models.ForeignKey(Event, null=True)
    product_key = models.ForeignKey(Product, null=True)
    name = models.CharField(max_length=50)
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)
    from_quantity = models.PositiveSmallIntegerField(null=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, null=False)
