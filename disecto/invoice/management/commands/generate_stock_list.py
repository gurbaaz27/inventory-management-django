from django.core.management.base import BaseCommand
from invoice.models import Item
from django.db.models import Q
from invoice.constants import STOCK_THRESHOLD
from invoice.serializers import ItemSerializer
from datetime import datetime, timedelta
from disecto.settings import MEDIA_ROOT

class Command(BaseCommand):
    help = "Auto generate a list of products/items with low stock/expiry from the inventory database."

    def handle(self, *args, **options):

        if Item.objects.filter(quantity__lte=STOCK_THRESHOLD).exists():
            items = ItemSerializer(Item.objects.filter(quantity__lte=STOCK_THRESHOLD), many=True).data

            with open(MEDIA_ROOT+"/stocklist.txt", "w") as f:
                f.write("Item ID, Description, Quantity\n")
                for item in items:
                    f.write(f"{item['id']}, {item['description']}, {item['quantity']}\n")
        else:
            with open(MEDIA_ROOT+"/stocklist.txt", "w") as f:
                f.write("Item ID, Description, Quantity\n")

        self.stdout.write('Generated list of products/items with low stock/expiry in media/stocklist.txt')