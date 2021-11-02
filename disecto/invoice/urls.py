from django.urls import path
from invoice import views


urlpatterns = [
    path('items/', views.ItemDetails.as_view(), name = "ItemDetails"),
    path('customers/', views.CustomerDetails.as_view(), name = "CustomerDetails"),
    path('customer-purchase/<int:id>', views.CustomerPurchase.as_view(), name = "CustomerPurchase"),
]