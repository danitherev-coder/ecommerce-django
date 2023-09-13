from django.shortcuts import render, get_object_or_404
from .models import Product
from categoryApp.models import Category

# Create your views here.
def store(request, category_slug=None):
  categories = None
  products = None

  if category_slug != None:
    # Obtener la categoria por medio del slug
    categories = get_object_or_404(Category, slug=category_slug)
    # Obtener los productos de la categoria
    products = Product.objects.filter(category=categories, is_available=True)
    # Obtener el numero de productos de la categoria
    product_count = products.count()
  else:
    # Obtener productos que esten disponibles
    products = Product.objects.all().filter(is_available=True)
    # Obtener el numero de productos
    product_count = products.count()

    
  return render(request, 'store/store.html', {
    'products': products,
    'product_count': product_count
  })


def product_detail(request, category_slug, product_slug):
  try:
    # en category__slug = uso doble guion bajo asi accedemos a campos relacionados en los modelos
    # En este caso, está accediendo al campo slug del modelo Category a través de una relación con el modelo Product.
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
  except Exception as e:
    raise e

  return render(request, 'store/product_detail.html', {
    'single_product': single_product
  })


