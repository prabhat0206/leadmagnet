from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name = "register"),
    path('user/<int:id>', VendorUser.as_view(), name = "add-permissions"),
    path('list', GetVendors.as_view(), name = "get-vendors"),
]
