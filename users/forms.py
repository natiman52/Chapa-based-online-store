from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from allauth.socialaccount.forms import SignupForm as socialAccountForm
class MyCustomSocialSignupForm(socialAccountForm):

    def save(self, request):
        user = super().save(request)
        return user
    
class customUserCreateForm(forms.ModelForm):
    age = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"text-dark"}))
    password1 = forms.CharField(label=_("Password"),widget=forms.PasswordInput(attrs={"class":"form-control mb-3 text-dark"}))
    password2 = forms.CharField(label=_("Password Confirmation"),widget=forms.PasswordInput(attrs={"class":"form-control text-dark"}))
    class Meta:
        model = User
        fields = ['name','phone',"location","age",'password1',"password2"]
        widgets = {
            "name":forms.TextInput(attrs={"class":"mb-3 text-dark flex"}),
            "phone":forms.TextInput(attrs={"class":"text-dark"}),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if(password1 != password2):
            raise forms.ValidationError(_("passwords didn't match."))
        return password2
class CustomSignupForm(SignupForm):
    phone = PhoneNumberField(region="ET")
    name =forms.CharField()
    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone_number).exists():
            raise forms.ValidationError(_("A user with this phone number already exists."))
        return phone_number

class PasswordForm(forms.Form):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"mb-4"}))
    password2 = forms.CharField(label="Confirm Password",help_text="Make sure you password is easy to remember. ",widget=forms.PasswordInput(attrs={"class":"mb-1"}))


    def clean_password2(self):
        if(self.cleaned_data['password1'] != self.cleaned_data['password2']):
            raise forms.ValidationError("passwords don't match")
        return self.cleaned_data['password2']


class FinishForm(forms.ModelForm):
    phone = forms.CharField(help_text="We will use this notification only")
    location=forms.CharField(help_text="This will later be used for delivery")
    class Meta:
        model = User
        fields = ['phone',"age","location"]
        widgets = {
            "name":forms.TextInput(attrs={"class":"mb-3 text-dark"}),
            "phone":forms.TextInput(attrs={"class":"text-dark"}),
        }


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email",'img','name','age','location']

    def clean_email(self):
        if(self.instance.socialconnected and self.cleaned_data.get("email")):
            raise forms.ValidationError("You cant change Email if you logged in using socialMedia")
        else:
            return self.cleaned_data.get("email")
        