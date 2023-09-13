from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
  category_name = models.CharField(max_length=200, unique=True)
  description = models.TextField(max_length=500, blank=True) # permite que el campo quede vacio
  slug = models.CharField(max_length=200, unique=True)
  cat_image = models.ImageField(upload_to='photos/categories', blank=True)

  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories' # Esto es para que en el admin se vea en plural porque por defecto toma el nombre de la clase y le asigna Categorys, cuando lo correcto es Categories

  # crear una url amigable
  def get_url(self):
    # products_by_category es el nombre de la url que se definio en storeApp/urls.py
    # reverse es una funcion de django que permite crear una url amigable
    return reverse('products_by_category', args=[self.slug])


  def __str__(self) -> str:
    return self.category_name