from django.shortcuts import render
from storeApp.models import Product

def home(request):
  products = Product.objects.all().filter(is_available=True)
  return render(request, 'home.html', {
    'products': products
  })