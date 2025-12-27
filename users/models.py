from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from .utils import generate_random_lower_string,generate_random_upper_string
from .managers import UserManager


def upload_to(instance,filename):
    return f"users/{instance.name}/" + filename
class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField(_("created"), db_index=True)
    modified = AutoLastModifiedField(_("modified"), db_index=True)

    class Meta:
        abstract = True
class User(AbstractBaseUser, PermissionsMixin,IndexedTimeStampedModel):
    email = models.EmailField(unique=True,null=True,blank=True)
    phone = PhoneNumberField(region="ET", unique=True,blank=True)
    temp_phone = PhoneNumberField(region="ET",blank=True,null=True)
    img = models.ImageField(upload_to=upload_to,default="default/profile/profile.jpg",null=True)
    name = models.CharField(max_length=225)
    age = models.IntegerField(blank=True,null=True)
    location = models.CharField(max_length=225,blank=True,null=True)
    sociallogin = models.BooleanField(default=False)
    socialconnected = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        default=False, help_text=_("Designates whether the user can log into this admin site.")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    emailaddress = None

    objects = UserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.name
class userCode(models.Model):
    link = models.CharField(max_length=225,default=generate_random_lower_string)
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    code = models.CharField(max_length=225,default=generate_random_upper_string)
    time = models.DateTimeField(auto_now=True)

class Notification(IndexedTimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.name}: {self.title or self.message[:20]}"