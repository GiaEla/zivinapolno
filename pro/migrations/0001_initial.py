# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-18 20:17
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ime')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Priimek')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Naslov')),
                ('city', models.CharField(blank=True, max_length=40, null=True, verbose_name='Kraj')),
                ('post', models.CharField(blank=True, max_length=40, null=True, verbose_name='Poštna številka')),
                ('token', models.CharField(db_index=True, max_length=15, null=True, unique=True, verbose_name='Token')),
                ('subscribed', models.CharField(blank=True, max_length=2, null=True, verbose_name='Obveščanje')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Dejavnost')),
                ('description', models.CharField(max_length=500, verbose_name='Opis')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='Slika')),
            ],
            options={
                'verbose_name_plural': 'dejavnost zavoda',
                'verbose_name': 'dejavnost zavoda',
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('account', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'bančni računi',
                'verbose_name': 'bančni račun',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(null=True, verbose_name='Pričetek')),
                ('date_to', models.DateField(null=True, verbose_name='Zaključek')),
                ('from_quantity', models.PositiveSmallIntegerField(default=0, verbose_name='Količinski popust')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Vrednost popusta')),
            ],
            options={
                'verbose_name_plural': 'Popusti',
                'verbose_name': 'Popust',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Generalni dogodek')),
                ('description', models.CharField(max_length=500, verbose_name='Opis')),
                ('date_from', models.DateField(null=True, verbose_name='Pričetek')),
                ('date_to', models.DateField(null=True, verbose_name='Zaključek')),
                ('independently_sold', models.BooleanField(default=False, verbose_name='Možen je nakup posamičnih vstopnic')),
            ],
            options={
                'verbose_name_plural': 'ustvari dogodek',
                'verbose_name': 'ustvari dogodek',
            },
        ),
        migrations.CreateModel(
            name='EventDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Dogodek')),
                ('date_from', models.DateField(null=True, verbose_name='Datum pričetka')),
                ('from_hour', models.TimeField(null=True, verbose_name='Ura pričetka')),
                ('date_to', models.DateField(null=True, verbose_name='Zaključek')),
                ('all_tickets', models.PositiveSmallIntegerField(null=True, verbose_name='Število vseh vstopnic')),
                ('event', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pro.Event', verbose_name='Generalni dogodek')),
            ],
            options={
                'verbose_name_plural': 'Dogodki',
                'verbose_name': 'Dogodek',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Datum')),
                ('invoice_number', models.PositiveIntegerField(editable=False, verbose_name='Račun')),
            ],
            options={
                'verbose_name_plural': 'računi',
                'verbose_name': 'račun',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Datum')),
                ('place', models.CharField(max_length=100, verbose_name='Kraj')),
                ('offer_number', models.PositiveIntegerField(editable=False, verbose_name='Predračun')),
                ('total_no_vat', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8, verbose_name='Znesek brez DDV')),
                ('total_with_vat', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8, verbose_name='Znesek z DDV')),
                ('total_with_discount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8, verbose_name='Znesek s popustom')),
                ('payed', models.BooleanField(default=False, verbose_name='Plačano')),
                ('pay_until', models.DateField(editable=False, null=True, verbose_name='Rok plačila')),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.BankAccount', verbose_name='Bančni račun')),
            ],
            options={
                'verbose_name_plural': 'predračuni',
                'verbose_name': 'predračun',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Izdelek')),
                ('description', models.CharField(max_length=500, verbose_name='Opis')),
                ('product_image', models.ImageField(null=True, upload_to='', verbose_name='Slika')),
                ('price_no_vat', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Cena brez DDV')),
                ('price_with_vat', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Cena z DDV')),
                ('vat', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='Cena z DDV')),
                ('event_based', models.BooleanField(default=True, verbose_name='Produkt je vezan na dogodek')),
            ],
            options={
                'verbose_name_plural': 'izdelki',
                'verbose_name': 'izdelek',
            },
        ),
        migrations.CreateModel(
            name='ProductEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold_tickets', models.SmallIntegerField(default=0, verbose_name='Število prodanih kart')),
                ('event_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.EventDetail', verbose_name='Dogodek')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.Product', verbose_name='Izdelek')),
            ],
            options={
                'verbose_name_plural': 'Izdelki, vezani na dogodek',
                'verbose_name': 'Izdelek, vezan na dogodek',
            },
        ),
        migrations.CreateModel(
            name='ProductQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qt_value', models.PositiveSmallIntegerField(default=0)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.Offer')),
                ('product', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Product')),
                ('product_event', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.ProductEvent')),
            ],
            options={
                'verbose_name_plural': 'količine izdelkov',
                'verbose_name': 'količina izdelka',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Ime')),
                ('reference', models.PositiveSmallIntegerField(verbose_name='Referenca')),
            ],
            options={
                'verbose_name_plural': 'bančne reference',
                'verbose_name': 'bančna referenca',
            },
        ),
        migrations.AddField(
            model_name='offer',
            name='products',
            field=models.ManyToManyField(through='pro.ProductQuantity', to='pro.Product', verbose_name='Izdelki'),
        ),
        migrations.AddField(
            model_name='offer',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Prejemnik'),
        ),
        migrations.AddField(
            model_name='offer',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.Reference', verbose_name='Referenca'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Offer', verbose_name='Predračun'),
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Product', verbose_name='izdelek'),
        ),
        migrations.AddField(
            model_name='discount',
            name='product_event',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.ProductEvent', verbose_name='izdelek, vezan na dogodek'),
        ),
    ]
