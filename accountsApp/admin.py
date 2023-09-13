from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# vamos a modificar como se muestra el usuario en el admin, porque cuando iniciamos sesion, solo nos sale el email y no su nombre, username, si esta activo o no
class AccountAdmin(UserAdmin):
  list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
  list_display_links = ('email', 'first_name', 'last_name') # para que los campos sean clickeables
  # campo que sea solo lectura y no se pueda modificar
  readonly_fields = ('last_login', 'date_joined')
  # ordenar de forma ascendente
  ordering = ('-date_joined',)

  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

# Register your models here.
admin.site.register(Account, AccountAdmin) # estamos pasando el modelo ACCOUNT y la clase que lo va a administrar