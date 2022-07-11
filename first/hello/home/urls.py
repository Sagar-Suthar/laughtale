from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index,name='home'),
    path('contact',views.contact,name='contact'),
    path('signup',views.signup,name='signup'),
    path('terms',views.terms,name='terms & privacy'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('shirts',views.shirts,name='shirts'),
    path('shoes',views.shoes,name='shoes'),
    path('jeans',views.jeans,name='jeans'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('update_item',views.updateItem,name='update_item'),
    path('process_order',views.processOrder,name='process_order')





]
