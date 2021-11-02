from django.db import models
from django.core.validators import RegexValidator
from .constants import PHONE_MESSAGE, PHONE_REGEX
import uuid

# Create your models here.
class Customer(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=100, unique=True)
    phoneno_regex   = RegexValidator(regex=PHONE_REGEX, message=PHONE_MESSAGE)
    phone           = models.CharField(validators=[phoneno_regex], max_length=17, blank=True)
    address         = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Item(models.Model):
    id              = models.AutoField(primary_key=True)
    description     = models.CharField(max_length=250, unique=True)
    price           = models.FloatField()
    quantity        = models.IntegerField()

    def __str__(self):
        return self.description


class Invoice(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer        = models.OneToOneField(Customer, on_delete=models.CASCADE)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name


class InvoiceItem(models.Model):
    invoice         = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item            = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity        = models.PositiveIntegerField(default=1)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice.customer.name + " : " + self.item.description
