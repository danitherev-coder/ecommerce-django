from django.shortcuts import render, get_object_or_404
from .models import Product
from categoryApp.models import Category
from cartsApp.models import CartItem
from cartsApp.views import _cart_id
# Importar el modulo de paginacion de django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def store(request, category_slug=None):
  categories = None
  products = None

  if category_slug != None:
    # Obtener la categoria por medio del slug
    categories = get_object_or_404(Category, slug=category_slug)
    # Obtener los productos de la categoria
    products = Product.objects.filter(category=categories, is_available=True, stock__gt=0)
    # Obtener el numero de productos de la categoria
    product_count = products.count()
    # paginacion para los productos de la categoria
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page) # g

  else:
    # Obtener productos que esten disponibles y que tengan stock
    products = Product.objects.all().filter(is_available=True, stock__gt=0)
    # Obtener el numero de productos
    product_count = products.count()

    # Paginar los productos
    # el primer parametro es la lista de productos(products) y el segundo es el numero de productos por pagina
    paginator = Paginator(products, 2)

    # como acceder a cada uno de esas paginas que estamos generando, por ejemplo si tenemos 15 products, mostramos solo 5 por pagina, entonces tendremos 3 paginas y para acceder a cada una de ellas usamos el metodo get
    page = request.GET.get('page') # el params page es el que definimos en el template store.html
    
    # Obtener los productos por pagina
    paged_products = paginator.get_page(page) # get_page es un metodo de paginator

  return render(request, 'store/store.html', {
    # ahora en lugar de enviar la lista de productos, enviamos los productos paginados
      # 'products': products,
    'products': paged_products,
    'product_count': product_count
  })


def product_detail(request, category_slug, product_slug):
  try:
    # en category__slug = uso doble guion bajo asi accedemos a campos relacionados en los modelos
    # En este caso, está accediendo al campo slug del modelo Category a través de una relación con el modelo Product.
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)

    # Logica para saber si el producto se encuentra en el carrito de compras
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

  except Exception as e:
    raise e

  return render(request, 'store/product_detail.html', {
    'single_product': single_product,
    'in_cart': in_cart
  })


