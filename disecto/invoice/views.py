from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from disecto.settings import MEDIA_ROOT
from django.http import HttpResponse, Http404
from .models import *
from .serializers import *
from .utils import create_invoice_pdf, construct_filename


class ItemDetails(APIView):
    """
    Retrieve or create items
    """
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(status=200, data=serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=f"Item {serializer.data['description']} successfully added")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
            

class CustomerDetails(APIView):
    """
    Retrieve or create customers
    """
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=f"Customer {serializer.data['name']} successfully added")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)


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
                filename                        = construct_filename(invoice.customer.name, invoice.timestamp)
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
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"No invoice found for customer {customer.name}. Create one using POST method.")


    def post(self, request, id, *args, **kwargs):
        customer = self.get_object(id)
        serializer = PurchaseSerializer(data=request.data, many=True)

        if serializer.is_valid():
            if Invoice.objects.filter(customer=customer).exists():
                invoice = Invoice.objects.get(customer=customer)
            else:
                invoice = Invoice.objects.create(customer=customer)

            for entry in serializer.data:
                if InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice).exists():
                    return Response(status=status.HTTP_403_FORBIDDEN, data=f"Item with id {entry['item']} already present in list. Use PUT method to update.")

            for entry in serializer.data:
                if not Item.objects.filter(id=entry["item"]).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND, data=f"No item found for id {entry['item']}")

            for entry in serializer.data:
                item = Item.objects.get(id=entry["item"])                

                if entry["quantity"] > item.quantity:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=f"Item with id {item.id} has insufficient stocks ({item.quantity})")
            
            for entry in serializer.data:
                item = Item.objects.get(id=entry["item"]) 
                InvoiceItem.objects.create(
                    invoice     = invoice,
                    item        = item,
                    quantity    = entry["quantity"]
                )
                item.quantity -= entry["quantity"]
                item.save()
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
                return Response(status=status.HTTP_404_NOT_FOUND, data=f"No invoice found for customer {customer.name}. Create one using POST method.")
            
            for entry in serializer.data:
                if not Item.objects.filter(id=entry["item"]).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND, data=f"No item found for id {entry['item']}")
            
            for entry in serializer.data:
                item = Item.objects.get(id=entry["item"])

                if InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice).exists():
                    invoice_item            = InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice)[0]
                    requested_quantity      = entry["quantity"] - invoice_item.quantity

                    if requested_quantity > item.quantity:
                        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=f"Item with id {item.id} has insufficient stocks ({item.quantity})")
                else:
                    if entry["quantity"] > item.quantity:
                        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=f"Item with id {item.id} has insufficient stocks ({item.quantity})")

            for entry in serializer.data:
                item = Item.objects.get(id=entry["item"])
                if InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice).exists():
                    invoice_item            = InvoiceItem.objects.filter(item__id=entry["item"], invoice=invoice)[0]
                    requested_quantity      = entry["quantity"] - invoice_item.quantity
                    invoice_item.quantity   = entry["quantity"]
                    invoice_item.save()
                    item.quantity -= requested_quantity
                    item.save()      
                else:
                    InvoiceItem.objects.create(
                        invoice     = invoice,
                        item        = item,
                        quantity    = entry["quantity"]
                    )   
                    item.quantity -= entry["quantity"]
                    item.save()

            return Response(status=status.HTTP_200_OK, data="List of items updated in purchase list successfully!")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)


class LowStockItemsList(APIView):
    """
    Retrieve low stock items list
    """
    def get(self, request, *args, **kwargs):
        filename                        = "stocklist.txt"
        path_to_file                    = MEDIA_ROOT + '/' + filename
        f                               = open(path_to_file, 'rb')
        textfile                        = File(f)
        response                        = HttpResponse(textfile.read(), content_type='text/plain')
        response['Content-Disposition'] = f'filename={filename}'
        return response
