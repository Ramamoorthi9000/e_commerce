from django.urls import path
from .views import *
app_name = "shop" 
urlpatterns = [
    path('',home_page,name="home"),
    path('collection/',collection_page),
    
    path('register/',register_page,name='register'),
    path('logout',logout_page,name="logout"),
    path('login/',login_page,name='login'),
    
    path('product_details/<str:name>',product_details,name='product_details'),
    path('product_show/<str:cname>/<str:pname>',product_show,name='product_show'),
    path('addtocart',add_to_cart,name="addtocart"),
    path('cart/',cart_page,name="cart"),
    path('favviewpage/',favviewpage,name="favviewpage"),



    path('fav',fav_page,name="fav"),
    path('remove_fav/<str:fid>',remove_fav,name="remove_fav"),
    path('remove_cart/<str:cid>',remove_cart,name="remove_cart"),

    ]