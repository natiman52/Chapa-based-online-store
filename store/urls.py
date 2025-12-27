from django.urls import path
from .views import home,catagorypage,add_cart,remove_cart,checkout,ProductDetail,cartview,AboutUS,Privacy,Terms,search

urlpatterns = [
    path('',home,name="home"),
    path('search',search,name="search"),
    path('search/<str:query>',search,name="search_query"),
    path('catagory/<str:catagory>',catagorypage,name="catagory"),
    path("add_cart/",add_cart,name="add-cart"),
    path("remove_cart/",remove_cart,name="remove-cart"),
    path("checkout",checkout,name="checkout"),
    path("product/<int:id>",ProductDetail,name="product-detail"),
    path('carts',cartview,name="cart_view"),
    path('about',AboutUS,name="about"),
    path('privacy',Privacy,name="privacy"),
    path("terms",Terms,name="terms"),
]