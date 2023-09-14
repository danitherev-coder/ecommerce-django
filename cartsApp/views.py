from django.shortcuts import render, redirect, get_object_or_404
from storeApp.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# Definir una funcion para obtener la session del usuario que tiene el carrito para obtener el ID del carrito
# por lo tanto para indicar que la funcion es privada se le agrega un guion bajo al inicio del nombre
def _cart_id(request):
  # session es un diccionario de python que se guarda en la base de datos y se guarda en el navegador del usuario como una cookie
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart

# crear carrito de compras para agregar productos
def add_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  # no sabemos si el carrito existe, asi que buscamos en un try
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # DoesNotExist es una excepcion que se lanza cuando no se encuentra el objeto
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
      cart_id = _cart_id(request)
    )
    cart.save()

  # ahora que tenemos el carrito, podemos agregar el producto
  try:
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
  except CartItem.DoesNotExist:
    cart_item = CartItem.objects.create(
      product = product,
      quantity = 1,
      cart = cart,
    )
    cart_item.save()

  return redirect('cart')

# funcion para remover un producto del carrito si la cantidad llega a ser menor a 1
def remove_cart(request, product_id):
  cart = Cart.objects.get(cart_id=_cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  # buscamos el item del carrito
  cart_item = CartItem.objects.get(product=product, cart=cart)

  if cart_item.quantity > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()

  return redirect('cart')

# Aca vamos a crear la funcion para que funcione el boton de eliminar del carrito, aca no aumentamos ni disminuimos la cantidad como en las 2 funciones anteriores
def remove_cart_item(request, product_id):
  # buscamos el carrito del usuario en la session actual _cart_id(request)
  cart = Cart.objects.get(cart_id=_cart_id(request))
  # buscamos el producto que queremos eliminar, si no existe, nos devuelve un 404
  product = get_object_or_404(Product, id=product_id)
  # buscamos el item del carrito
  cart_item = CartItem.objects.get(product=product, cart=cart)
  cart_item.delete()

  return redirect('cart')


# renderizar el carrito con datos
def cart(request, total = 0, quantity = 0, cart_items = None):

  try:
    # buscamos el carrito gracias a la session del usuario
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # buscamos los items del carrito
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    # iteramos sobre los items del carrito para obtener el total y la cantidad
    for cart_item in cart_items:
      # += es igual a total = total + (cart_item.product.price * cart_item.quantity)
      total += (cart_item.product.price * cart_item.quantity)
      # += es igual a quantity = quantity + cart_item.quantity
      quantity += cart_item.quantity
    
    # Vamos a aplicar impuestos
    tax = (2 * total)/100
    grand_total = total + tax

  except ObjectDoesNotExist: # ObjectDoesNotExist es una excepcion que se lanza cuando no se encuentra el objeto
    pass # ignora la excepcion

  return render(request, 'store/cart.html', {
    'total': total,
    'quantity': quantity,
    'cart_items': cart_items,
    'tax': tax,
    'grand_total': grand_total,
  })