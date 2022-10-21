from django.urls import path
from .views import create_customer, login_customer, logout_customer, process_order, register_customer, store, cart, checkout, update_item
urlpatterns = [
    path("",store, name = "store"),
    path("cart",cart, name = "cart"),
    path("checkout",checkout, name = "checkout"),
    path("update_item",update_item,name = "update_item"),
    path("process-order",process_order,name = "process_order"),
    
    #this urls are for members info
    path("register",register_customer,name = "register"),
    path("login",login_customer,name = "login"),
    path("logout",logout_customer,name = "logout"),
    path("create-customers-account",create_customer,name ="create_customer_account")
            ]