from django.db import models

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    product_type=models.CharField(max_length=100)
    measuring_unit=models.CharField(max_length=50,null=True,blank=True)
    stock_quantity=models.DecimalField(max_digits=10,decimal_places=2)
    cost_price=models.DecimalField(max_digits=10,decimal_places=2)
    selling_price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self) :
        return self.product_name


class Bill(models.Model):
    customer_name=models.CharField(max_length=100)
    billing_date=models.DateField(auto_now_add=True)
    billing_time=models.TimeField(auto_now_add=True)
    paid=models.BooleanField(default=False)
    bill_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self) :
        return self.customer_name

class BillItems(models.Model):
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.DecimalField(max_digits=10,decimal_places=2,default=0.00,null=True,blank=True)
    net_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

class FirmInfo(models.Model):
    firm_name = models.CharField(max_length=255)
    firm_image = models.ImageField(upload_to='qr_code/', null=True, blank=True)
    firm_gst=models.CharField(max_length=20,null=True)
    firm_mob1=models.CharField(max_length=11,null=True)
    firm_mob2=models.CharField(max_length=11,null=True)
    firm_add=models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.firm_name
    
class ProductType(models.Model):
    product_type=models.CharField(max_length=120)

    def __str__(self):
        return self.product_type