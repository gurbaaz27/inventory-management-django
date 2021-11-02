from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

class InvoiceItemAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)