from django.urls import path
from .views import my_profile,showprofile,update_account,changepassword,changePhone,activatephone,webhook,unpaidBills,my_deliveries

urlpatterns = [
    path('',my_profile,name="my-profile"),
    path('profile',showprofile,name="profile-detail"),
    path("edit-profile",update_account,name="profile-update"),
    path('change-password',changepassword,name="change-password"),
    path("change-phone",changePhone,name='change-phone'),
    path("activate-phone/<str:link>",activatephone,name="activate-phone"),
    path('webhook/',webhook,name="webook"),
    path("unpaid-biils",unpaidBills,name="unpaid-bills"),
    path("deliveries",my_deliveries,name="my-deliveries")

]