
from django.contrib.auth.forms import UserCreationForm
import json
from django.shortcuts import render
from datetime import datetime
from sqlalchemy import false
from home.models import Contact, Order,Signup
from django.contrib.auth import authenticate,login
from django.contrib import auth
from .models import *
from .models import User    
from django.http import JsonResponse
import datetime

# Create your views here.
def index(request):
    return render(request,'loggedout.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        contact=Contact(name=name,email=email,message=message,date=datetime.today())
        contact.save()
        return render(request,'loggedout.html')

    return render(request,'contact.html')

def signup(request):
    form=UserCreationForm()
    if request.method=="POST":
       form =UserCreationForm(request.POST)
       if form.is_valid():
           form.save()
           x=form.cleaned_data.get('username')
           customer=Customer(name=x)
           customer.save()
           return render(request,'loggedout.html',{'msg':'account created'})
        # name=request.POST.get('name')
        # email=request.POST.get('email')
        # password=request.POST.get('password')
        # repeat_password=request.POST.get("password_repeat") 
        # context = { 'variable':'wrong password',
        # 'name' :"successfully signup. you can login now" }
        # if password==repeat_password:    
        #     signup=User(email=email,password=password,username=name)
        #     signup.save()
            
        #     return render(request,'loggedout.html',context)
        # elif password!=repeat_password:
        #     return render(request,"signup.html",context)

    return render(request,'signup.html',{'form':form})

    
def terms(request):
    return render(request,'terms & privacy.html')
    
def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        
        if user is not None:
            context={
                        'name':f'Welcome {username}'
                    }
            auth.login(request,user)
            return render(request,'loggedout.html',context)
        else:
            context={
                        'variable':'Incorrect details'
                    }
            return render(request,'login.html',context)

    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return render(request,'loggedout.html')

def shirts(request):
    shirts=Product.objects.filter(type='Shirts')
    context={'shirts':shirts}
    return render(request,'shirts.html',context)

def shoes(request):
    shoes=Product.objects.filter(type='Shoes')
    context={'shoes':shoes}
    return render(request,'shoes.html',context)

def jeans(request):
    jeans=Product.objects.filter(type='Jeans')
    context={'jeans':jeans}
    return render(request,'jeans.html',context)
    
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer 
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items={}
        order={'get_cart_total':0,'get_cart_items':0}
  
    context={'items':items,'order':order}
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer 
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}
  
    context={'items':items,'order':order}
    return render(request,'checkout.html',context)
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('productId:',productId )

    print('Action:',action)

    customer=request.user.customer
    product =Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
           
    orderItem,created= OrderItem.objects.get_or_create(order=order,product=product)
    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action =='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
                                                                
                    
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total =float(data['form']['total'])
        order.transaction_id=transaction_id

        if total== order.get_cart_total:
            order.complete=True
        order.save()
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    else: 
        print('not logged in')
    return JsonResponse('payment complete !',safe=False)
