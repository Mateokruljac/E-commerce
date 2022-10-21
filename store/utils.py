from .models import *
import json

def cookieCart(request):
    cartItem = 0
    total = 0
    shipping = False 
    try:
        cart = json.loads(request.COOKIES["cart"])
        print(cart)
    except:
        cart = {}
    
    items = []
    for i in cart:
        
        try:    
           product = Product.objects.get(pk = i) 
           cartItem += cart[i]["quantity"]
           total += (product.price * cart[i]["quantity"])
           
           item = {
               "product":{
                   "id" : product.id,
                   "name" : product.name,
                   "price": product.price,
                   "digital": product.digital,
                   "image" : product.image,
               },
               "quantity" : cart[i]["quantity"],
               "total_price" : total
           }
           items.append(item)
           
        
        except : 
            pass
    print("Cookie:",cart)
    context = {"items":items,"full_total_price":total,"cartItems":cartItem,"shipping":shipping}
    return context

def guestOrder (request,data):
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
    return " "