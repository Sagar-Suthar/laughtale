from django.contrib import admin
from .models import *

from home.models import Contact, Signup
# Register your models here.
admin.site.register(Contact)
admin.site.register(Signup)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)