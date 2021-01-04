from django.urls import path
from . import views

urlpatterns = [
     path("",views.home,name = "home"),
     path('login/',views.login_user,name = "login"),
     path('logout/',views.logout_user,name = "logout"),
     path('register/',views.register_user,name = "register"),
     path('myshop/',views.myshop,name = "myshop"),
     path('product/delete/<int:id>/',views.delete_product,name = 'delete_product'),
     path('product/add/',views.add_product,name = "add_product"),
     path('shops/',views.shops,name = "shops"),
     path('shops/<int:id>/',views.shop,name = "shop"),
     path('cart/',views.cart,name = "cart"),
     path('product/addtocart/<int:id>',views.add_to_cart,name = "add_to_cart"),
     path('order/',views.order,name = "order"),
 ]
 