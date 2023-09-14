# Es una funcion global que se ejecuta cada vez que se carga una pagina
from .models import Cart, CartItem
from .views import _cart_id

# Funcion para obtener el numero de productos en el carrito y mostrarlo en el navbar
def counter(request):
  cart_count = 0

  try:
    cart = Cart.objects.filter(cart_id=_cart_id(request))
    # Obtener un carrito de compras por usuario
    cart_items = CartItem.objects.all().filter(cart=cart[:1])
    # Recorrer los productos del carrito de compras
    for cart_item in cart_items:
      cart_count += cart_item.quantity
  except Cart.DoesNotExist:
    cart_count = 0
  
  return dict(cart_count=cart_count)