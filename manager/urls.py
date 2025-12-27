from django.urls import path
from .views import adminhome,admin_product,create_product,OrderView,change_promote_status,update_product,customer_list,customer_detail,delivery_list

urlpatterns = [
    path('',adminhome, name='adminhome'),
    path('products',admin_product, name='admin_product'),
    path("create-product",create_product,name="create_product"),
    path("orders",OrderView,name='orders'),
    path("products/<int:id>",change_promote_status,name="change_promote_status"),
    path("products/<int:id>/update",update_product,name="update_product"),
    path("customers",customer_list,name="customers"),
    path("customers/<int:id>",customer_detail,name="customer_detail"),
    path("deliveries",delivery_list,name="deliveries"),

]