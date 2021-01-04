from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm , UserProfileForm ,StoreForm ,ProductForm
from .models import Product , Store , CartItem , Bill
# Create your views here.

def home(request):
    return render(request,'shop/index.html')

def login_user(request):
    if request.method == "GET":
        return render(request,'shop/login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            return redirect('/login')

@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


def register_user(request):

    if request.method == "GET":
        user_form = UserForm()
        user_profile_form = UserProfileForm()
        return render(request,'shop/register.html',{
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
        store_form = StoreForm()
        product_form = ProductForm()
        return render(request,'shop/myshop.html',{
            "store_form" : store_form,
            "product_form" : product_form
        })
    
    else:

        store = StoreForm(request.POST)
        store = store.save(commit=False)
        store.owner = request.user
        store.save()
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
        product.store = request.user.store
        product.save()
    return redirect('/myshop')


def shops(request):
    if request.user.is_authenticated:
        shops  = Store.objects.filter(pincode = request.user.profile.pincode)
    else:
        shops = Store.objects.all()

    
    return render(request,'shop/shops.html',{
            "shops":shops
        })

def shop(request,id):
    shop = Store.objects.get(id = id)

    return render(request,"shop/shop.html",{
        "shop":shop
    })


@login_required
def cart(request):
    cart_items = request.user.cartitem_set.all()
    cart_all = cart_items
    cart_grouped = []
    # get current list of shops user is ordering from
    store_ids = set([item.product.store.id for item in cart_items])
    for store_id in store_ids:
        #find store
        store = Store.objects.get(id = store_id)
        #find all items brought from a store
        items = []
        for cart_item in cart_all:
            if cart_item.product.store.id == store_id:
                items.append(cart_item)
        # print(store)
        # print(items)
        cart_grouped.append({"store" : store,"items" : items})
    # print(cart_grouped)
    return render(request,'shop/cart.html',{
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
    shop_id = int(request.POST["shop_id"])
    deliver = request.POST.get("deliver")
    if deliver == "on":
        deliver=True
    else:
        deliver = False

    print(deliver)
    print(shop_id)
    for item in request.user.cartitem_set.all():
        print(item.product.store.id)
        if item.product.store.id == shop_id:
            print(item)
            price+= item.quantity * item.product.price
            item.delete()
    
    shopped_from = Store.objects.get(id = shop_id)
    bill  = Bill(address = address,user=request.user,total_price=price,deliver=deliver,store=shopped_from)
    bill.save()

    return HttpResponse(f"Order Placed! \n Total price {bill.total_price}")
