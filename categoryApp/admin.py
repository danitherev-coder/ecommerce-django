from django.contrib import admin
from .models import Category

# Clase para generar que el slug se genere automaticamente
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    # Mostrar en la tabla los siguientes datos
    list_display = ('category_name', 'slug')


# Register your models here.
admin.site.register(Category, CategoryAdmin)