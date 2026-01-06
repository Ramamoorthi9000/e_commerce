from django.shortcuts import render,redirect
from .models import *
from .form import *
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home_page(request):
   products = Catagory.objects.filter(status=False)
   return render(request,'home.html',{'products': products})
 
def collection_page(request):
    products = Catagory.objects.filter(status=False)
    return render(request,'collection.html',{'products': products})



def product_details(request, name):
    products = product.objects.filter(category__name=name, category__status=False)

    if not products.exists():
        messages.warning(request, f"No products found for category '{name}'.")
    return render(request, 'product.html', {'products': products})

def product_show(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products=product.objects.filter(name=pname,status=0).first()           
            return render(request,"products_show.html",{'products':products})
        else:
            messages.error(request,"no such catagory found")
            return redirect("products.html")
    else:
        messages.error(request,"no such catagory found")
        return redirect("products.html")
        
def register_page(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"register.html",{'form':form})
  

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/register/")
  

def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login/")
    return render(request,"login.html")
   
  
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'},status=200)
        else:
          if product_status.qantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'},status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'},status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'},status=200)
   else:
    return JsonResponse({'status':'Invalid Access'},status=200)
  
  
  
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage/")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart/")
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)