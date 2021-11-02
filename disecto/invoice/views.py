from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.files import File
from disecto.settings import MEDIA_ROOT
from django.http import HttpResponse, Http404
from .models import *
from .serializers import *
from .utils import create_invoice_pdf


class ItemDetails(APIView):
    """
    Retrieve, update or delete an item.
    """
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(status=200, data=serializer.data)


class CustomerPurchase(APIView):
    """
    Retrieve, update or delete a customers list of items.
    """
    def get_object(self, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            raise Http404


    def get(self, request, id, *args, **kwargs):
        customer = self.get_object(id)
        if Invoice.objects.filter(customer=customer).exists():
            invoice                         = Invoice.objects.get(customer=customer)

            if InvoiceItem.objects.filter(invoice=invoice).exists():
                invoice_items                   = InvoiceItemsSerializer(InvoiceItem.objects.filter(invoice=invoice), many=True)
                invoice_info                    = InvoiceSerializer(invoice)
                filename                        = f"{customer.name}-{invoice.timestamp}"
                path_to_file                    = MEDIA_ROOT + '/' + filename
                create_invoice_pdf(path_to_file, invoice_info.data, invoice_items.data)
                f                               = open(path_to_file + '.pdf', 'rb')
                pdfFile                         = File(f)
                response                        = HttpResponse(pdfFile.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'filename={filename}.pdf'
                return response
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data=f"No item put to purchase list")
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"No invoice found for customer {customer.name}")


    def post(self, request, id, *args, **kwargs):
        customer = self.get_object(id)
        serializer = PurchaseSerializer(data=request.data, many=True)

        if serializer.is_valid():
            if Invoice.objects.filter(customer=customer).exists():
                invoice = Invoice.objects.get(customer=customer)
            else:
                invoice = Invoice.objects.create(customer=customer)

            for entry in serializer.data:
                if Item.objects.filter(id=entry["item"]).exists():
                    item = Item.objects.get(id=entry["item"])
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND, data=f"No item found for id {entry['item']}")

                if InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice).exists():
                    return Response(status=status.HTTP_403_FORBIDDEN, data=f"Item with id {entry['item']} already present in list. Use PUT method to update.")

                InvoiceItem.objects.create(
                    invoice     = invoice,
                    item        = item,
                    quantity    = entry["quantity"]
                )
            return Response(status=status.HTTP_200_OK, data="List of items added to purchase list successfully!")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)


    def put(self, request, id, *args, **kwargs):
        customer = self.get_object(id)
        serializer = PurchaseSerializer(data=request.data, many=True)

        if serializer.is_valid():
            if Invoice.objects.filter(customer=customer).exists():
                invoice = Invoice.objects.get(customer=customer)
            else:
                invoice = Invoice.objects.create(customer=customer)

            for entry in serializer.data:
                
                if not Item.objects.filter(id=entry["item"]).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND, data=f"No item found for id {entry['item']}")

                if InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice).exists():
                    invoice_item            = InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice)[0]
                    invoice_item.quantity   = entry["quantity"]
                    invoice_item.save()
                else:
                    item = Item.objects.get(id=entry["item"])
                    InvoiceItem.objects.create(
                        invoice     = invoice,
                        item     = item,
                        quantity    = entry["quantity"]
                    )   

            return Response(status=status.HTTP_200_OK, data="List of items updated in purchase list successfully!")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

