# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from django.urls import reverse


class Prices(models.Model):

    url = models.ForeignKey('Urls', models.CASCADE, related_name='data')
    date = models.DateTimeField(auto_now_add=True)
    current_price = models.IntegerField(null=True)
    old_price = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'prices'
        verbose_name='Price'
        verbose_name_plural='Prices'
        ordering=['date', 'id']


class Urls(models.Model):

    url = models.TextField(unique=True)
    name = models.CharField(max_length=255, default='Undefiend name')
    product_photo = models.ImageField(
        upload_to='product',
        default='default.png'
    )
    archive = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('info', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.id}: {self.url}'

    class Meta:
        db_table = 'urls'
        verbose_name='Product'
        verbose_name_plural='Products'
        ordering=['id']
