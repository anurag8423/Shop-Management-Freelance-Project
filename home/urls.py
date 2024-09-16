from django.urls import path
from . import views

urlpatterns = [
    path('',views.billing,name="billing"),
    path('itemAdd/',views.itemAdd,name="itemAdd"),
    path('itemList/',views.itemList,name="itemList"),
    path('calBill/<str:bid>/',views.calculateBill,name="calculateBill"),
    path('transactionHistory/',views.billHistory,name="billHistory"),
    path('itemEdit/<str:pid>/',views.itemEdit,name="itemEdit"),
    path('billReceipt/<str:bid>/',views.billReceipt,name="billReceipt")
]
