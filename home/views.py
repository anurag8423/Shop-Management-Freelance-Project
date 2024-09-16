from django.shortcuts import render
from datetime import datetime
from decimal import Decimal
from .models import *


def billing(request):
    if request.method=='POST':
        customer_name=request.POST.get('customer_name')
        ins=Bill(customer_name=customer_name)
        ins.save()
        current_date=datetime.now()
        bills=Bill.objects.filter(billing_date=current_date).order_by('-billing_time')
        context={'creation':True,'bills':bills}
        return render(request,'billing.html',context)
    
    current_date=datetime.now()
    bills=Bill.objects.filter(billing_date=current_date).order_by('-billing_time')
    context={'creation':False,'bills':bills}
    return render(request,'billing.html',context)

def itemAdd(request):
    producttypes=ProductType.objects.all()
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        product_type=request.POST.get('product_type')
        stock_quantity=request.POST.get('stock_quantity')
        cost_price=request.POST.get('cost_price')
        selling_price=request.POST.get('selling_price')
        measuring_unit=request.POST.get('measuring_unit')
        
        if product_type is None:
            context={'information':True,'message':'Please select the type of the product being added','success':'info','types':producttypes}
            return render(request,'itemAdd.html',context)
        
        if measuring_unit is None:
            context={'information':True,'message':'Please select the measuring unit of the product being added','success':'info','types':producttypes}
            return render(request,'itemAdd.html',context)
        
        cost=Decimal(cost_price)
        sell=Decimal(selling_price)
        if cost>=sell:
            context={'information':True,'message':'There is no profit margin in this product','success':'warning','types':producttypes}
            return render(request,'itemAdd.html',context)
        
        product=Product.objects.filter(product_name__iexact=product_name)
        if product.exists():
            context={'information':True,'message':'The product already exists in the product list','success':'warning','types':producttypes}
            return render(request,'itemAdd.html',context)
        else:
            ins=Product(product_name=product_name,product_type=product_type,stock_quantity=stock_quantity,cost_price=cost_price,selling_price=selling_price,measuring_unit=measuring_unit)
            ins.save()
            context={'information':True,'message':'The new product is successfully added to the product list','success':'success','types':producttypes}
            return render(request,'itemAdd.html',context)
        
    context={'information':False,'message':'','success':'','types':producttypes}
    return render(request,'itemAdd.html',context)

def itemList(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'itemList.html',context)

def calculateBill(request,bid):
    producttypes=ProductType.objects.all()
    current_bill=Bill.objects.get(id=bid)
    billitems=BillItems.objects.filter(bill=current_bill)
    if request.method=='GET':
        product_type=request.GET.get('product_type')
        if product_type==None:
            context={'searched':False,'type':'','products':None,'bill':current_bill,'billItems':billitems,'alert':False,'message':'','types':producttypes}
            return render(request,'bill.html',context)
        elif product_type=='all':
            products=Product.objects.all()
            context={'searched':True,'products':products,'type':'all','bill':current_bill,'billItems':billitems,'alert':False,'message':'','types':producttypes}
            return  render(request,'bill.html',context)
        else:
            products=Product.objects.filter(product_type=product_type)
            context={'searched':True,'products':products,'type':product_type,'bill':current_bill,'billItems':billitems,'alert':False,'message':'','types':producttypes}
            return render(request,'bill.html',context)
        
    elif request.method=='POST':
        productid=request.POST.get('productid')
        quantity=request.POST.get('quantity')
        product_type=request.POST.get('type')
        itemid=request.POST.get('itemid')

        if quantity is None and productid is None and product_type is None and itemid is None:
            current_bill.paid=True
            current_bill.save()
            context={'searched':False,'type':'','products':'','bill':current_bill,'billItems':billitems,'alert':True,'message':'The bill is payment is confirmed successfully','types':producttypes}
            return render(request,'bill.html',context)
        
        products=Product.objects.all()
        if product_type !='all':
            products=Product.objects.filter(product_type=product_type)

        if itemid is not None and productid is None and product_type is not None:
            billitem=BillItems.objects.get(id=itemid)
            billed_product=billitem.product
            billed_product.stock_quantity=billed_product.stock_quantity+billitem.quantity
            billed_product.save()
            current_bill.bill_amount=current_bill.bill_amount-billitem.net_amount
            current_bill.save()
            billitem.delete()
            billitems=BillItems.objects.filter(bill=current_bill)
            context={'searched':True,'type':product_type,'products':products,'bill':current_bill,'billItems':billitems,'alert':True,'message':'The specified item is successfully deleted from the bill','types':producttypes}
            return render(request,'bill.html',context)
        
        quant=Decimal(quantity)
        if quant <=0:
            context={'searched':True,'type':product_type,'products':products,'bill':current_bill,'billItems':billitems,'alert':True,'message':'Product quantity should not be less than or equal to zero.','types':producttypes}
            return render(request,'bill.html',context)
        
        product=Product.objects.get(id=productid)
        if product.stock_quantity < quant:
            context={'searched':True,'type':product_type,'products':products,'bill':current_bill,'billItems':billitems,'alert':True,'message':'Available product quantity is less than the required quantity.','types':producttypes}
            return render(request,'bill.html',context)
        
        product.stock_quantity=product.stock_quantity-quant
        net_amt=product.selling_price*quant
        ins=BillItems(bill=current_bill,product=product,quantity=quant,net_amount=net_amt)
        current_bill.bill_amount=current_bill.bill_amount+net_amt
        ins.save()
        product.save()
        current_bill.save()
        billitems=BillItems.objects.filter(bill=current_bill)

        context={'searched':True,'type':product_type,'products':products,'bill':current_bill,'billItems':billitems,'alert':True,'message':'Product is succesfully added to the bill','types':producttypes}
        return render(request,'bill.html',context)
    
        
    context={'searched':False,'type':'','products':None,'bill':current_bill,'billItems':billitems,'alert':False,'message':'','types':producttypes}
    return render(request,'bill.html',context)


def billHistory(request):

    if request.method=='POST':
        print("Reached here")
        name=request.POST.get('customer_name')
        date=request.POST.get('billing_date')

        if date is not None:
            bills=Bill.objects.filter(billing_date=date).order_by
            bill_date=str(date)
            context={'bills':bills,'heading':f"Transactions dated {bill_date}"}
            return render(request,'billHistory.html',context)

        elif name is not None:
            bills=Bill.objects.filter(customer_name__icontains=name)|Bill.objects.filter(customer_name__iexact=name)
            context={'bills':bills,'heading':f"Transaction with customer name similar to {name}"}
            return render(request,'billHistory.html',context)
        
    bills=Bill.objects.all().order_by('-billing_date')
    context={'bills':bills,'heading':'Transaction History'}
    return render(request,'billHistory.html',context)

def itemEdit(request,pid):
    producttypes=ProductType.objects.all()
    product=Product.objects.get(id=pid)
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        product_type=request.POST.get('product_type')
        stock_quantity=request.POST.get('stock_quantity')
        cost_price=request.POST.get('cost_price')
        selling_price=request.POST.get('selling_price')
        measuring_unit=request.POST.get('measuring_unit')
        
        product.product_name=product_name
        product.product_type=product_type
        product.stock_quantity=stock_quantity
        product.cost_price=cost_price
        product.selling_price=selling_price
        product.measuring_unit=measuring_unit
        product.save()

        context={'information':True,'message':'The product details are changed successfully','success':'success','product':product,'types':producttypes}
        return render(request,'itemEdit.html',context)
        
    context={'information':False,'message':'','success':'info','product':product,'types':producttypes}
    return render(request,'itemEdit.html',context)

def billReceipt(request,bid):
    current_bill=Bill.objects.get(id=bid)
    if request.method == 'POST':
        current_bill.paid=True
        current_bill.save()
        billitems=BillItems.objects.filter(bill=current_bill)
        context={'bill':current_bill,'billitems':billitems,'alert':True}
        return render(request,'billReceipt.html',context)
    
    billitems=BillItems.objects.filter(bill=current_bill)
    context={'bill':current_bill,'billitems':billitems,'alert':False}
    return render(request,'billReceipt.html',context)