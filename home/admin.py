from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(BillItems)
admin.site.register(FirmInfo)
admin.site.register(ProductType)