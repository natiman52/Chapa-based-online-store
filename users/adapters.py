from typing import Tuple
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import User
from phonenumber_field.phonenumber import PhoneNumber
from django.urls import reverse
from django.core.files import File
import tempfile
from urllib.request import urlretrieve

class customSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        return super().get_connect_redirect_url(request, socialaccount)
    def is_auto_signup(self, request, sociallogin):
        return True  # Automatically create users
    def pre_social_login(self, request, sociallogin):
        return True
    def populate_user( self, request,sociallogin,data):
        user = super().populate_user(request, sociallogin, data)
        user.sociallogin = True
        if not user.name:
            if name := data.get("name"):
                user.name = name
            elif first_name := data.get("first_name"):
                user.name = first_name
                if last_name := data.get("last_name"):
                    user.name += f" {last_name}"
        return user
    
    def save_user(self, request, sociallogin, form=None):
        file =urlretrieve(url=sociallogin.serialize()['account']['extra_data']['picture'])
        sociallogin.user.socialconnected = True
        sociallogin.user.img.save("social.png", File(open(file[0],'rb')))
        return super().save_user(request, sociallogin, form)

class PhoneNumberAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self,request):
        print(request.GET)
        return "/"
    def get_signup_redirect_url(self, request):
        if(request.user.sociallogin == True):
            return reverse("accounts_finish")
        return super().get_signup_redirect_url(request)
    def is_open_for_signup(self, request):
        # Allow signup via phone number
        return True
    def save_user(self, request, user, form, commit=True):
        # Save phone number from the form if it's present
        print("test ing")
        phone_number = form.cleaned_data.get('phone')
        name = form.cleaned_data.get("name")
        if not phone_number:
            raise ValidationError(_('Phone number is required.'))
        if not name:
            raise ValidationError(_('Name is required.'))
        user.phone= phone_number
        user.name = name
        user.is_active = False
        if "password1" in form.cleaned_data:
            password = form.cleaned_data["password1"]
        elif "password" in form.cleaned_data:
            password = form.cleaned_data["password"]
        else:
            password = None
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def get_phone(self, user) -> Tuple[str, bool] | None:
        return (str(user.phone),False)
    def set_phone(self, user, phone: str, verified: bool):
        user.phone = PhoneNumber.from_string(phone).as_international.replace(" ","")
    def set_phone_verified(self, user, phone: str):
        return True
    def get_user_by_phone(self, phone: str):
        phone_nu = PhoneNumber.from_string(phone).as_international.replace(" ","")
        user =User.objects.filter(phone=phone_nu)
        if user.exists():
            return user[0]
        else:
            return None
