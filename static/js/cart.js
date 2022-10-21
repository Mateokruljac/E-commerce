// result is all buttons on the page 
var updateButtons = document.getElementsByClassName("update-cart")

// console.log("CSRF",csrftoken)
for (var i =0;i < updateButtons.length; i++){
    // for every click, we will get productID and action etc. "add"
        updateButtons[i].addEventListener("click",function(){
            var productID = this.dataset.product
            var action = this.dataset.action
            console.log("product id:",productID,"product action:",action)
      
            console.log("User:",user)
            // if user is authenticated
            if (user == 'AnonymousUser'){
                addCookieItem(productID,action)
            }
            // if user is not authenticated
            else{
              updateUserOrder(productID,action)
            }
        })                              
}

// create function with parameters productID and action
function updateUserOrder(productID,action){
    console.log("User is logged in, sending data...")
    // url view we created before
    var url = "update_item"
    
    fetch(url,{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "X-CSRFToken"  : csrftoken,
        },
        body :JSON.stringify({
            "productID" : productID,
            "action" : action 
        })
    })
    // .then returns promise to fetch
    .then((response) => {

        return response.json();
    })
    .then((data) => {
        // location.reload()
        conslole.log(data)
    });
}



function addCookieItem(productID,action){
    console.log("Hi,You are not logged in\nBut producti ID is",productID,"and action",action)
    
    if (action == "add"){
        
        //if action is add
        if(cart[productID] == undefined){
            //productID is key and {"quantity" : num} is value of query 
            cart[productID] = {"quantity":1}
            cart[productID]["quantity"] = 1
        }
        else{
            cart[productID]["quantity"] += 1
        }
    
    }  
        //if action is removed
        if (action == "remove"){
            cart[productID]["quantity"] -= 1;
            
            //delete from cart if quantity is equal or less 0
            if (cart[productID]["quantity"] == 0){
                console.log("Remove item",cart[productID]["id"]);
                delete cart[productID]
            }
        }
    
        console.log("Cart",cart)
        document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
        location.reload()
        
    }
    

