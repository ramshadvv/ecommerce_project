from django.contrib import admin

from accounts.models import Accounts, CustomerAdress

# Register your models here.
admin.site.register(Accounts)
admin.site.register(CustomerAdress)