from django.db import models
from storeApp.models import Product

# Create your models here.
class Cart(models.Model):
  cart_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)

  def __str__(self) -> str:
    return self.cart_id
  

class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)

  def sub_total(self):
    return self.product.price * self.quantity

  # Calcular el sub_total de produtos por ejemplo, precio unitario de pc = 100 por la cantidad(quantity) de 2, el sub_total seria 200
  def sub_total(self):
    return self.product.price * self.quantity

  # unicode es una funcion que sirve para mostrar el nombre del producto en el admin de django
  def __unicode__(self):
    return self.product



