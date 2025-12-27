
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.phonenumber import PhoneNumber
class PhoneOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username, password=None, **kwargs):
        UserModel = get_user_model()
        phon = PhoneNumber.from_string(username,region="ET")
        try:
            # Attempt to find the user by phone number or username
            if(phon.is_valid()):
                user = UserModel.objects.get(
                    models.Q(phone=phon.as_international.replace(" ",""))
                )
            else:
                user = UserModel.objects.get(
                    models.Q(phone=username)
                )                
        except UserModel.DoesNotExist:
            # Return None if the user does not exist
            return None

        # Check the password
        if user.check_password(password):
            return user
        return None
    