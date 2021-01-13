from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm , UserProfileForm ,ShopForm ,ProductForm
from .models import Product , Shop , CartItem , Bill
# Create your views here.

def home(request):
    return render(request,'unishop/index.html')


def login_user(request):
    if request.method == "GET":
        return render(request,'unishop/login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            return render(request,'unishop/login.html',{"message":"Invalid Credentials. Please try again"})

@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


def register_user(request):

    if request.method == "GET":
        user_form = UserForm()
        user_profile_form = UserProfileForm()
        return render(request,'unishop/register.html',{
            "user_form":user_form,
            "user_profile_form":user_profile_form
        })

    else:

        user = UserForm(request.POST)
        user_profile = UserProfileForm(request.POST)

        if user.is_valid() and user_profile.is_valid():

            user = user.save(commit= False)
            user.set_password(user.password)
            user.save()

            user_profile = user_profile.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return redirect('/login')

        else:
            print("Validation failed")

            return redirect('/register')


        

@login_required
def myshop(request):

    if not request.user.profile.is_owner:
        return redirect('/')

    if request.method == "GET":
        shop_form = ShopForm()
        product_form = ProductForm()
        return render(request,'unishop/myshop.html',{
            "shop_form" : shop_form,
            "product_form" : product_form
        })
    
    else:

        shop = ShopForm(request.POST)
        shop = shop.save(commit=False)
        shop.owner = request.user
        shop.save()
        return redirect('/myshop')

@login_required
def delete_product(request,id):
    if not request.user.profile.is_owner:
        return redirect('/')

    Product.objects.get(pk=id).delete()
    return redirect('/myshop')
    
@login_required
def add_product(request):
    if not request.user.profile.is_owner:
        return redirect('/')

    product = ProductForm(request.POST)

    if product.is_valid():

        product = product.save(commit=False)
        product.shop = request.user.shop
        product.save()
    return redirect('/myshop')


def shops(request):
    if request.user.is_authenticated:
        shops  = Shop.objects.filter(pincode = request.user.profile.pincode)
    else:
        shops = Shop.objects.all()

    
    return render(request,'unishop/shops.html',{
            "shops":shops
        })

def shop(request,id):
    shop = Shop.objects.get(id = id)

    return render(request,"unishop/shop.html",{
        "shop":shop
    })


@login_required
def cart(request):
    cart_items = request.user.cartitem_set.all()
    cart_all = cart_items
    cart_grouped = []
    # get current list of shops user is ordering from
    shop_ids = set([item.product.shop.id for item in cart_items])
    for shop_id in shop_ids:
        #find shop
        shop = Shop.objects.get(id = shop_id)
        #find all items brought from a shop
        items = []
        for cart_item in cart_all:
            if cart_item.product.shop.id == shop_id:
                items.append(cart_item)
        # print(shop)
        # print(items)


# item -> product 

        total = sum (item.product.price for item in items)
        cart_grouped.append({"shop" : shop,"items" : items , "total" : total})
    # print(cart_grouped)

    # cart items [ {shop , [items ... ] , total} , ...]
    return render(request,'unishop/cart.html',{
        "cart_items" : cart_grouped
    })


@login_required
def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    
    try:
        old_item = request.user.cartitem_set.get(product = product,user = request.user)
        old_item.quantity+=1
        old_item.save()
    except:
        new_item = CartItem(product=product,user = request.user , quantity= 1)
        new_item.save()

    return redirect('/cart')

@login_required
def order(request):
    price = 0
    address = request.user.profile.address
    #shop from which ordered
    shop_id = int( request.POST.get("shop_id"))
    deliver = request.POST.get("deliver")
    if deliver == "on":
        deliver=True
    else:
        deliver = False

    print(deliver)
    print(shop_id)
    for item in request.user.cartitem_set.all():
        print(item.product.shop.id)
        #only cart items belonging to that shop
        if item.product.shop.id == shop_id:
            print(item)
            price+= item.quantity * item.product.price

            #update product quantity
            item.product.quantity = item.product.quantity - item.quantity
            item.product.save()
            item.delete()
    
    shopped_from = Shop.objects.get(id = shop_id)
    bill  = Bill(address = address,user=request.user,total_price=price,deliver=deliver,shop=shopped_from)
    bill.save()

    return HttpResponse(f"Order Placed! \n Total price {bill.total_price}")

@login_required
def shop_orders(request):
    if not request.user.profile.is_owner:
        return redirect('/')
    
    orders = request.user.shop.bills.all()

    return render(request,'unishop/shop_orders.html',{
        "orders" : orders
    })

##user orders
@login_required
def orders(request):

    orders = request.user.bill.all()
    return render(request,"unishop/orders.html",{
        "orders":orders
    })