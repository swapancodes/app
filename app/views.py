from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced

class ProductView(View):
   def get(self, request):
      topwears=Product.objects.filter(category='TW')
      bottomwears=Product.objects.filter(category='BW')
      laptops=Product.objects.filter(category='L')
      mobiles=Product.objects.filter(category='M')
      return render(request, 'home.html', {'topwears':topwears,'bottomwears':bottomwears,'laptops':laptops,'mobiles':mobiles} )

class ProductDetailView(View):
  def get(self, request, pk):
    product=Product.objects.get(pk=pk)
    return render(request,"productdetail.html", {'product':product})



def mobile(request, data=None):
  if data==None:
     mobiles=Product.objects.filter(category='M')
  elif data=='Redmi' or data=='Samsung':
     mobiles=Product.objects.filter(category='M').filter(brand=data)
  elif data=='below':
     mobiles=Product.objects.filter(category='M').filter(discount_price__lt=10000)
  elif data=='above':
     mobiles=Product.objects.filter(category='M').filter(discount_price__gt=10000)
  return render(request,"mobile.html", {'mobiles':mobiles})


from .forms import CustomerRegistrationForm
from django.contrib import messages

class CustomerRegistrationView(View):
  def get(self, request):
     form=CustomerRegistrationForm()
     return render (request, 'customerregistration.html', {'form':form})
  def post(self, request):
      form=CustomerRegistrationForm(request.POST)
      if form.is_valid():
        messages.success(request, 'Congratulation! Register Successfully')
        form.save()
      return render (request, 'customerregistration.html', {'form':form})

from django.contrib.auth import logout
from django.shortcuts import redirect
class LogoutView(View):
     def get (self, request):
         logout(request)                 
         return redirect('login')

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
def password_change(request): 
    if request.method=="POST":
       form=PasswordChangeForm(user=request.user, data=request.POST)  
       if form.is_valid():
          form.save()
          update_session_auth_hash(request,form.user)
          messages.success(request, 'Congratulation! Changed Successfully')
          return redirect('profile')        
    else:
       form=PasswordChangeForm(user=request.user)
    return render (request, 'changepassword.html',{'form':form} )

       
from .forms import CustomerProfileForm
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
   def get(self, request):
      form=CustomerProfileForm()
      return render (request, 'profile.html', {'form':form})
   def post(self, request):
      form=CustomerProfileForm(request.POST)
      if form.is_valid():
         user=request.user
         name=form.cleaned_data['name']
         locality=form.cleaned_data['locality']
         city=form.cleaned_data['city']
         zipcode=form.cleaned_data['zipcode']
         state=form.cleaned_data['state']
         data=Customer(user=user, name=name, locality=locality, city=city, zipcode=zipcode, state=state )
         data.save()
         messages.success(request, 'Congratulation! Profile Updated Successfully')
      return render (request, 'profile.html', {'form':form})

@login_required
def address(request):
   add=Customer.objects.filter(user=request.user)
   return render(request,'address.html',{'add':add})


@login_required
def AddToCart(request):
   user=request.user
   product_id=request.GET.get('prod_id')
   product=Product.objects.get(id=product_id)
   Cart(user=user, product=product).save()
   return redirect('show-cart')


@login_required
def ShowCart(request):
    if request.user.is_authenticated:
       user=request.user
       cart=Cart.objects.filter(user=user)
       amount=0.0
       shipping_amount=100.0
       total_amount=0.0
       cart_product=[p for p in Cart.objects.all() if p.user==request.user]
       if cart_product:
          for p in cart_product:
             temp_amount=(p.quantity * p.product.discount_price)
             amount += temp_amount
             total_amout= amount + shipping_amount
          return render(request, 'addtocart.html', {'carts':cart, 'total_amout':total_amout, 'amount':amount})
       else: 
 
          return render(request, 'emptycart.html')
@login_required
def CheckOut(request):
   user=request.user
   add=Customer.objects.filter(user=request.user)
   cart_items=Cart.objects.filter(user=request.user)
   amount=0.0
   shipping_amount=100.0
   total_amount=0.0
   cart_product=[p for p in Cart.objects.all() if p.user==request.user]
   if cart_product:
      for p in cart_product:
          temp_amount=(p.quantity * p.product.discount_price)
          amount += temp_amount
          total_amout= amount + shipping_amount  
      return render(request,'checkout.html',{'add':add,'total_amout':total_amout,'cart_items':cart_items})
   
@login_required
def PaymentDone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required
def Orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'order.html',{'order_placed':op})


from django.db.models import Q
from django.http import JsonResponse
def plus_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount=0.0
      shipping_amount=100.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
      if cart_product:
         for p in cart_product:
            temp_amount=(p.quantity * p.product.discount_price)
            amount += temp_amount
            total_amout= amout + shipping_amount
         data={'quantity':c.quantity, 'amount':amount, 'total_amout':total_amout}
         return JsonResponse(data)

def minus_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity-=1
      c.save()
      amount=0.0
      shipping_amount=100.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
      if cart_product:
         for p in cart_product:
            temp_amount=(p.quantity * p.product.discount_price)
            amount += temp_amount
            total_amout= amout + shipping_amount
         data={'quantity':c.quantity, 'amount':amount, 'total_amout':total_amout}
         return JsonResponse(data)

def remove_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))      
      c.delete()
      amount=0.0
      shipping_amount=100.0
      total_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
      if cart_product:
         for p in cart_product:
            temp_amount=(p.quantity * p.product.discount_price)
            amount += temp_amount
            total_amout= amout + shipping_amount
         data={'amount':amount, 'total_amout':total_amout}
         return JsonResponse(data)