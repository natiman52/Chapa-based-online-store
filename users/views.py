from django.shortcuts import render,redirect
from .forms import customUserCreateForm,PasswordForm,FinishForm,UpdateProfile
from django.urls import reverse
from .models import User,userCode
from store.models import Payment,PaymentLink,Rating
from django.contrib.auth.decorators import login_required
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib import messages
from django.http import HttpResponse
from selltools import chapa
from django.contrib.auth import logout
from render_block import render_block_to_string
import time
from .utils import generate_random_lower_string,is_profile_complete
def Signup(request):
    form =customUserCreateForm()
    if request.method == "POST":
        form = customUserCreateForm(request.POST)
        if form.is_valid():
            phon = form.cleaned_data["phone"]
            user =User(name=form.cleaned_data['name'],phone=phon)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.age = form.cleaned_data["age"]
from django.shortcuts import render,redirect
from .forms import customUserCreateForm,PasswordForm,FinishForm,UpdateProfile
from django.urls import reverse
from .models import User,userCode
from store.models import Payment,PaymentLink,Rating
from django.contrib.auth.decorators import login_required
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib import messages
from django.http import HttpResponse
from selltools import chapa
from django.contrib.auth import logout
from render_block import render_block_to_string
import time
from .utils import generate_random_lower_string,is_profile_complete
def Signup(request):
    form =customUserCreateForm()
    if request.method == "POST":
        form = customUserCreateForm(request.POST)
        if form.is_valid():
            phon = form.cleaned_data["phone"]
            user =User(name=form.cleaned_data['name'],phone=phon)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.age = form.cleaned_data["age"]
            user.location = form.cleaned_data["location"]
            user.save()
            usercode,created=userCode.objects.get_or_create(user=user)
            print(usercode.link)
            return redirect(f"{reverse('account_verification',kwargs={'id':user.id})}")
        else:
            return render(request,"account/signup.html",{"form":form,"login_url":reverse("account_login"), "title": "Sign Up"})
    return render(request,"account/signup.html",{"form":form,"login_url":reverse("account_login"), "title": "Sign Up"})

def Verify(request,link):
    cod_obj = userCode.objects.filter(link=link).first()
    if(cod_obj):
        cod_obj.user.is_active = True
        cod_obj.user.save()
        cod_obj.delete()
        return render(request,'account/verify.html', {"title": "Account Verification"})
    else:
        messages.error(request,"something went wrong, please contact support","danger")
        return redirect("/")

def resend_OTP(request,id):
    cod_obj = userCode.objects.filter(user__id=id).first()
    cod_obj.link = generate_random_lower_string()
    cod_obj.save()
    messages.success(request,"New SMS has been sent")
    html = render_block_to_string("account/verification.html","body",{'id':id},request=request)
    return HttpResponse(html)

def passwordreset(request):
    if request.method == "POST":
        if(request.POST.get('login')):
            phone = PhoneNumber.from_string(request.POST.get('login'),region="ET").as_international
            user = User.objects.filter(phone=phone).first()
            
            if(user):
                
                cod = userCode.objects.create(user=user)
                ## do some sinding
                return redirect(f"{reverse('account_verification',kwargs={'id':user.id})}")
            else:
               
                return render(request,"account/password-reset.html",{"errors":True, "title": "Reset Password"})
    return render(request,"account/password-reset.html", {"title": "Reset Password"})
    
def passwordResetChange(request,link):
    cod_obj = userCode.objects.filter(link=link).first()
    if(cod_obj):
        form =PasswordForm()
        if request.method == "POST":
            form = PasswordForm(request.POST)
            if(form.is_valid()):
                cod_obj.user.set_password(request.POST.get('password1'))
                cod_obj.user.save()
                cod_obj.delete()
                messages.success(request,"Password has been seccessfully changed")
                return redirect(reverse('account_login'))    
            return render(request,"account/passwordchange.html",{"form":form, "title": "Change Password"})
        return render(request,"account/passwordchange.html",{"form":form, "title": "Change Password"})
    else:
        messages.error(request,"something went wrong, please contact support","danger")
        return redirect("/")

@login_required
def FinsihSocialSignUp(request):
    if(not request.user.sociallogin):
        return redirect(reverse('home'))
    form =FinishForm()
    if request.method == "POST":
        form = FinishForm(request.POST,request.FILES,instance=request.user)
        if(form.is_valid()):
            request.user.sociallogin = False
            form.save()
            return redirect(reverse("home"))
        return render(request,"account/finishaccount.html",{"form":form, "title": "Finish Account Setup"})
    return render(request,"account/finishaccount.html",{"form":form, "title": "Finish Account Setup"})

@login_required
@is_profile_complete
def my_profile(request):
    time.sleep(3)
    items = Payment.objects.filter(user=request.user,status="success")
    if(request.GET.get("search") or request.GET.get("sort")):
        if(request.GET.get("search")):
            items = items.filter(product__name__icontains=request.GET.get("search"))
        if(request.GET.get("sort")):
            if(request.GET.get("sort") == "date"):
                items = items.order_by(f"{request.GET.get('sort')}")
            else:
                items = items.order_by(f"product__{request.GET.get('sort')}")
        html = render_block_to_string("users/profile/components/transaction.html","transaction_block",{"items":items},request=request)
        return HttpResponse(html)
    if(request.method == "POST"):
        print(request.POST.get("payment"))
        if(request.POST.get("rating")):
            pay_obj = Payment.objects.filter(id=int(request.POST.get("payment")),user=request.user).first()
            if(pay_obj):
                Rating.objects.create(user=request.user,product=pay_obj.product,rate=int(request.POST.get("rating")))
                messages.success(request,"Thank you for your feedback")
            items = Payment.objects.filter(user=request.user,status="success")
            html = render_block_to_string("users/profile/components/transaction.html","transaction_block",{"items":items},request=request)
            return HttpResponse(html)
    return render(request,"users/profile/main.html",{'items':items, "title": "My Profile"})

@login_required
@is_profile_complete
def showprofile(request):
    return render(request,"users/profile/myprofile.html", {"title": "My Profile"})

@login_required
def account_logout(request):
    logout(request)
    messages.error(request,"account loged out")
    return redirect(reverse("home"))

@login_required
@is_profile_complete
def update_account(request):
    form = UpdateProfile(instance=request.user)
    form2 = PasswordForm()
    if(request.session.get('form2')):
        form2 = PasswordForm(request.session.get('form2'))
        del request.session['form2']
    if(request.method == "POST"):
        form = UpdateProfile(request.POST,instance=request.user)
        if(form.is_valid()):
            messages.success(request,"Profile successfully updated")
            form.save()
            return redirect("/")
    return render(request,"users/profile/editprofile.html",{'form':form,"form2":form2, "title": "Edit Profile"})

@login_required
@is_profile_complete
def changepassword(request):
    form2 = PasswordForm()
    if(request.method == "POST"):
        form2 = PasswordForm(request.POST)
        if(form2.is_valid()):
            request.user.set_password(request.POST.get('password1'))
            request.user.save()
            messages.success(request,"Password hase been changed")
            return redirect(reverse('account_login'))
        request.session["form2"] = form2.data
        return redirect(reverse("profile-update"))
    

@login_required
@is_profile_complete
def changePhone(request):
    if(request.method =="POST"):        
        request.user.temp_phone = request.POST.get('phone')
        request.user.save()
        cod_obj,status = userCode.objects.get_or_create(user=request.user)
        cod_obj.link = generate_random_lower_string()
        cod_obj.save()
        # url will be 'activate phone'
        messages.success(request,"A link has been sent to the new phone number. Please verify")
        html =render_block_to_string("allauth/layouts/base.html","messages_block",{},request=request)
        response = HttpResponse(html)
        return response
    

@login_required
@is_profile_complete
def activatephone(request,link):
    cod_obj = userCode.objects.filter(link=link).first()
    cod_obj.user.phone = cod_obj.user.temp_phone
    cod_obj.user.save()
    del cod_obj
    messages.success(request,"Phone number has been changed")
    return render(request,"users/profile/phonechanged.html", {"title": "Phone Changed"})
@login_required
@is_profile_complete
def unpaidBills(request):
    items = PaymentLink.objects.filter(user=request.user).order_by("date")
    if(request.POST):
        if(request.POST.get("delete")):
            objs = PaymentLink.objects.get(id=int(request.POST.get("delete")),user=request.user)
            for i in filter(None, objs.txt.split("_")):
                pas= Payment.objects.filter(id=int(i))
                if(pas.exists()):
                    pas[0].delete()
            objs.delete()
            items = PaymentLink.objects.filter(user=request.user).order_by("date")
            messages.success(request,"Unpaid bill has been deleted")
            html = render_block_to_string("users/profile/components/unpaidC.html","unpaid_block",{'items':items},request=request)
            return HttpResponse(html)
    return render(request,"users/profile/unpaid.html",{'items':items, "title": "Unpaid Bills"})

def webhook(request):
    trx = request.GET.get("trx_ref")
    test = chapa.Verify(trx)
    if(test.get("status") == "success"):
        obj = list(filter(None, trx.split("_")))
        PaymentLink.objects.get(txt=trx).delete()
        pay_objs =Payment.objects.filter(id__in=[int(i) for i in obj])
        for pay_obj in pay_objs:
            pay_obj.status = "success"
            pay_obj.save()
        
    return HttpResponse("<h1></h1>")

@login_required
@is_profile_complete
def my_deliveries(request):
    items = Payment.objects.filter(user=request.user, status="success", delivery_on=True).order_by("-date")
    return render(request, "users/profile/deliveries.html", {'items': items, "title": "My Deliveries"})