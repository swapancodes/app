from django.contrib import admin

# Register your models here.
from .models import(Customer, Product, Cart, OrderPlaced)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display=['id','title','selling_price','discount_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
  list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
  list_display=['id','user','customer','product','quantity','order_date','status']










