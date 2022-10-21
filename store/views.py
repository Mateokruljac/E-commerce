from .models import Product, Order, OrderItem, Customer, ShippingAddress
from .utils import cookieCart
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
import json
import datetime
# Create your views here.

#store view
def store (request):
    products = Product.objects.all()
    if request.user.is_authenticated:
       customer = request.user.customer
       #get requested order. If not exists, then create
       order,creatd = Order.objects.get_or_create(customer = customer,complete = False)
       #get all items that have order as parent
       items = order.orderitem_set.all()
       cartItems = order.get_total_items
    else: 
        cartItems = 0
        try:
            cart = json.loads(request.COOKIES["cart"])
        except: 
            cart = {}
        for i in cart:
            cartItems += cart[i]["quantity"] 
        order = {"get_total_items": cartItems,"shipping":False}
        cartItems = order["get_total_items"]
    context = {"products":products,"cartItems":cartItems,"order":order}
    return render (request,"store/store.html",context)

#cart view
def cart (request):
    shipping = False
    full_total_price = 0 
    if request.user.is_authenticated:
       customer = request.user.customer
       #get requested order. If not exists, then create
       order,creatd = Order.objects.get_or_create(customer = customer,complete = False)
       #get all items that have order as parent
       items = order.orderitem_set.all()
       cartItem = order.get_total_items

       # get total price of all items 
       total_price_per_item = [item.product.price*item.quantity for item in items]
       for x in total_price_per_item:
           full_total_price += x
    else:
        cookie_data = cookieCart(request)
        items = cookie_data["items"]
        full_total_price = cookie_data["full_total_price"]
        cartItem = cookie_data["cartItems"]
        shipping = cookie_data["shipping"] 
        print("Full_total_price", full_total_price)
    
    context = {"items":items,"full_total_price":full_total_price,"cartItems":cartItem,"shipping":shipping}
    return render (request,"store/cart.html",context)

#checkout view 
def checkout (request):
    if request.user.is_authenticated:
       customer = request.user.customer
       #get requested order. If not exists, then create
       order,created = Order.objects.get_or_create(customer = customer,complete = False)
       #get all items that have order as parent
       cartItems = order.get_total_items
       items = order.orderitem_set.all()
       shipping = order.shipping
       # get total price of all items 
       full_total_price = 0 
       total_price_per_item = [item.product.price*item.quantity for item in items]
       for x in total_price_per_item:
            full_total_price += x
       context = {"items":items,"full_total_price":full_total_price,"cartItems":cartItems,"shipping":shipping,"order":order}

    else: 
        cookie_data = cookieCart(request)
        items = cookie_data["items"]
        full_total_price = cookie_data["full_total_price"]
        cartItems = cookie_data["cartItems"]
        shipping = cookie_data["shipping"] 
        digitals = []
        
        for i in range(len(items)):
            product = items[i]
            digitals.append(product["product"]["digital"])
        
        if False in digitals:
            shipping = True

               
        context = {"items":items,"full_total_price":full_total_price,"cartItems":cartItems,"shipping":shipping}
    return render (request,"store/checkout.html",context)

def update_item (request):
    data = json.loads(request.body)
    product_ID = data["productID"]
    action = data["action"]
    # print("Product",product_ID,"\nAction",action)
    
    customer = request.user.customer
    product = Product.objects.get(pk = product_ID)  
    
    #why get_or_create?
    #because we have to change valeue of orderItem
    order,created = Order.objects.get_or_create(customer = customer, complete = False)
    print("Created:",order)
    order_item, created =  OrderItem.objects.get_or_create(order = order,product = product) 
    
    #add or remove a item
    if action == "add":
        order_item.quantity = order_item.quantity + 1 
        
    
    elif action == "remove":
        order_item.quantity = order_item.quantity - 1
    
    print("ORDER",order_item.quantity)
    order_item.save()
    
    if order_item.quantity <= 0:
        order_item.delete()     
    
    return JsonResponse("Item was added",safe = False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        
        #check inputs of shipping fields etc. Create a shipping (address) with parsed data 
        if order.shipping == True:
           ShippingAddress.objects.create(
               customer = customer,
               order = order,
               address = data["shipping"]["address"],
               city = data["shipping"]["city"],
               state = data["shipping"]["state"],
               zip_code = data["shipping"]["zipcode"]
           ).save()
    else:
        print("User is not logged in !")
        print("COOKIES:",request.COOKIES["cart"])
        username = data["form"]["name"]
        email = data["form"]["email"]
        cookieData= cookieCart(request)
        items = cookieData["items"]
        
        #it is neccessery to automatically create a new customer, 
        # check if user with that username or email already exits
        if Customer.objects.filter(email = email).exists() or  Customer.objects.filter(name = username).exists():
            pass
        else:
            customer = Customer.objects.create(
                email = email,
                name = username,
            )
            customer.save()
        
        #create a order
        order = Order.objects.create(
            customer = customer,
            complete = False
        ),
        
        for item in items:
            product = Product.objects.get(id = item["product"]["id"])        
            orderItem = OrderItem.objects.get_or_create(
                product = product,
                order = order,
                quantity = item["quantity"]
            )
        
        if order.shipping == True:
           ShippingAddress.objects.create(
               customer = customer,
               order = order,
               address = data["shipping"]["address"],
               city = data["shipping"]["city"],
               state = data["shipping"]["state"],
               zip_code = data["shipping"]["zipcode"]
           ).save()
    
    total = float (data["form"]["total"])
    order.transaction_id = transaction_id
    
    #user must be unable to manimulate with num of items
    print("TOTAL 1",total) 
    print("TOTAL 2",order.get_total_items) 
    if int(total) == int(order.get_total_items):
        order.complete = True
    order.save()
    return JsonResponse("Process order is submitted!",safe = False)


#register costumer to E-commerce website
def register_customer (request):
    cartItems = 0
    if request.method ==  "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        checkbox = request.POST.get("checkbox")
        
        if password1 == password2:
            if User.objects.filter(email = email).exists() or User.objects.filter(username = username).exists():
                messages.info(request,"Sorry, user with that username or password already exists. Please use another!")
                return render (request,"members/register.html",{"cartItems":cartItems})
            else:
                if str(checkbox) == "on":
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        username = username,
                        password = password1,
                    )
                    user.save()
                    messages.success(request,"New account successfully created!")
                    return redirect("login")
                    
                else:
                    messages.info(request,"Please, accept all statements in Term of services. Thank you!")
                    return render (request,"members/register.html",{"cartItems":cartItems})
        else:
            messages.warning(request,"Password not matching!")
            return render (request,"members/register.html",{"cartItems":cartItems})
        
    else:
        return render(request,"members/register.html",{"cartItems":cartItems})

def login_customer(request):
    cartItems = 0
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        #chek user input 
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            if request.user != request.user.customer.user:
               return redirect("create_customer_account")
            else: 
                products = Product.objects.all() 
                customer = request.user.customer
                #get requested order. If not exists, then create
                order,creatd = Order.objects.get_or_create(customer = customer,complete = False)
                #get all items that have order as parent
                items = order.orderitem_set.all()
                cartItems = order.get_total_items
                context = {"products":products,"cartItems":cartItems}
                return redirect("store")

        else: 
            messages.info(request,"Invalid username or password. Try again or use another account!")
            return render (request,"members/login.html",{"cartItems":cartItems})
        
    else:
        return render (request,"members/login.html",{"cartItems":cartItems})
    
    
def logout_customer(reqeust):
    logout(reqeust)
    return redirect("login")

def create_customer (request):
    user = request.user
    name = request.user.username
    email = request.user.email
    #check if tjatt customer exist
    if Customer.objects.filter(user = user,name = name, email = email).exists():
         return redirect("store")
    else:
       customer = Customer.objects.create(user = user,name = name, email = email)
       customer.save()
       return redirect("store")    
