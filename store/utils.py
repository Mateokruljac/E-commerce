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
    return " "