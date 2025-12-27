from django.shortcuts import render
from .models import Catagory,StoreDiscount,Product,Cart,Payment,PaymentLink,Discounts,Image
from django.db import transaction,models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from render_block import render_block_to_string
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from selltools import chapa
from users.utils import getDeliveryPrice
import json
from .forms import CartSerializer

# Create your views here.
def search(request, query=None):
    if request.GET.get("search"):
        return HttpResponseRedirect(f"/search/{request.GET.get('search')}")
        
    pag = Product.objects.all()
    if query:
        pag = pag.filter(name__icontains=query)
        
    if (request.GET.get("price_range")):
        pag = pag.filter(price__range=[0,int(request.GET.get("price_range"))])
    if(request.GET.get("sort")):
        match request.GET.get("sort"):
            case "newest":
                pag = pag.order_by("-date")
            case "oldest":
                pag =pag.order_by("date")
            case "price_asc":
                pag =pag.order_by("price")
            case "price_desc":
                pag =pag.order_by("-price")
    
    paginator = Paginator(pag, 12)
    page = request.GET.get('page')
    try:
        pag_obj = paginator.page(page)
    except PageNotAnInteger:
        pag_obj = paginator.page(1)
    except EmptyPage:
        pag_obj = paginator.page(paginator.num_pages)

    context = {
        "items": pag_obj,
        "catagories": Catagory.objects.all(),
        'hot': Product.objects.filter(promoted=True)[:4],
        "title": f"Search Results for {query}" if query else "Search Results",
    }
    return render(request, "search.html", context)

def home(request):
    pag =Product.objects.all()
    if(request.GET.get("search")):
        pag = pag.filter(name__icontains=request.GET.get("search"))
    if (request.GET.get("price_range")):
        pag = pag.filter(price__range=[0,int(request.GET.get("price_range"))])
    if(request.GET.get("sort")):
        match request.GET.get("sort"):
            case "newest":
                pag = pag.order_by("-date")
            case "oldest":
                pag =pag.order_by("date")
            case "price_asc":
                pag =pag.order_by("price")
            case "price_desc":
                pag =pag.order_by("-price")
    
    paginator = Paginator(pag, 12) # Show 12 items per page
    page = request.GET.get('page')
    try:
        pag_obj = paginator.page(page)
    except PageNotAnInteger:
        pag_obj = paginator.page(1)
    except EmptyPage:
        pag_obj = paginator.page(paginator.num_pages)

    context = {
        "items": pag_obj,
        "catagories": Catagory.objects.all(),
        "heroes": StoreDiscount.objects.all(),
        'hot':Product.objects.filter(promoted=True)[:4],
        "deals":Discounts.objects.all()[:2],
        "title": "Home",
    }
    return render(request,"home.html",context)

@require_POST
def add_cart(request):
    try:
        obj = Product.objects.get(id=int(request.POST.get('id')))
        Cart.objects.get_or_create(user=request.user,product=obj)
        html = render_block_to_string("component/topcart.html","cart",request=request)
        return HttpResponse(html)
    except:
        messages.error(request,"Something went wrong please try again",'danger')
        html = render_block_to_string("allauth/layouts/base.html",'messages_block',request=request)
        response =  HttpResponse(html)
        response['HX-Retarget'] = "#messagesContainer"
        return response

@require_POST
def remove_cart(request):
    try:
        obj = Product.objects.get(id=int(request.POST.get('id')))
        ca = Cart.objects.get(user=request.user,product=obj)
        ca.delete()
        html = render_block_to_string("component/topcart.html","cart",request=request)
        return HttpResponse(html)
    except:
        messages.error(request,"Something went wrong please try again",'danger')
        html = render_block_to_string("allauth/layouts/base.html",'messages_block',request=request)
        response =  HttpResponse(html)
        response['HX-Retarget'] = "#messagesContainer"
        return response


def catagorypage(request,catagory):
    obj =Product.objects.filter(catagory__name=catagory)
    if(request.GET.get("sort")):
        match request.GET.get("sort"):
            case "newest":
                obj =obj.order_by("-date")
            case "oldest":
                obj =obj.order_by("date")
            case "price_asc":
                obj =obj.order_by("price")
            case "price_desc":
                obj =obj.order_by("-price")
    if(request.GET.get("search")):
        obj = obj.filter(name__icontains=request.GET.get("search"))
    if (request.GET.get("price_range")):
        obj = obj.filter(price__range=[0,int(request.GET.get("price_range"))])
    pag = Paginator(obj,28)
    try:
        pag_obj = pag.page(request.GET.get("page"))
    except PageNotAnInteger:
        pag_obj = pag.page(1)
    except EmptyPage:
        pag_obj = pag.page(pag.num_pages)

    context ={
        "catagories": Catagory.objects.all(),
        "heroes": StoreDiscount.objects.all(),
        "items": pag_obj,
        'hot':Product.objects.filter(promoted=True)[:4],
        "title": f"{catagory} Products",
    }
    return render(request,"catagories.html",context)


@login_required
def checkout(request):
    if(request.method == "POST"):
        items=list(filter(None,request.POST['items'].split(',')))
    elif (request.method == "GET"):
        items =list(filter(None,request.GET.get('items').split(',')))
    ## Rendering page starts   
    products = Product.objects.filter(id__in=[int(i.split("-")[0]) for i in items])
    total_pay = 0 
    for i in products:
        res = [t.split('-')[1] for t in items if str(i.id) == t.split('-')[0]]
        i.amm=int(res[0])
        total_pay += i.amm * i.price
    sub_total = total_pay
    delivery_price = getDeliveryPrice(products,request.user.location)
    tax =(total_pay+delivery_price) * 0.08
    total_pay+= getDeliveryPrice(products,request.user.location)
    total_pay+= tax
    if request.method == "POST":
        total = ""
        delivery = request.POST.get('delivery_on')
        for i in items:
            pay=Payment(user=request.user,product_id=int(i.split('-')[0]),quantity=int(i.split('-')[1]))
            total += f"{pay.id}_"
        if(not delivery):
            total_pay -= delivery_price
        else:
            pay.delivery_on = True
        pay.save()
        chapa_response = chapa.InitiatePayment(total,total_pay,request.user)
        if(chapa_response['status'] == "failed"):
            return HttpResponse("<h1><h1>")
        PaymentLink.objects.create(user=request.user,link=chapa_response["data"]["checkout_url"],amount=total_pay,txt=total)
        return HttpResponseRedirect(chapa_response["data"]["checkout_url"])
    return render(request,"checkout.html",{"items":products,"delivery":delivery_price,"all":total_pay,"tax":tax,"sub_total":sub_total, "title": "Checkout"})

def cartview(request):
    if(request.method == "POST"):
        if(request.POST.get("remove")):
            delate = request.user.carts.filter(product__id=int(request.POST.get("remove")))[0]
            delate.delete()
    query = Image.objects.filter(product=models.OuterRef("product")).values("img")[:1]
    products = request.user.carts.all().annotate(quantity=models.Value(1)).annotate(img=models.Subquery(queryset=query)).annotate(max_quantity=models.F("product__quantity"))
    seri_data = CartSerializer(products,many=True).data
    if(request.method == "POST"):
        html = render_block_to_string("cart.html","remove_cart",request=request,context={"products":products,"products_list":json.dumps(seri_data)})
        response =HttpResponse(html)
        return response
    return render(request,"cart.html",{"products":products,"products_list":json.dumps(seri_data), "title": "Your Cart"})


def ProductDetail(request,id):
    product = Product.objects.get(id=id)
    product_related = Product.objects.filter(catagory__in=product.catagory.all()).exclude(id=product.id).distinct()[:5]
    print(product_related)
    boughted_by = product.boughted_by.filter(status="success")
    if(request.user.is_authenticated):
        def addView():
            product.views.add(request.user)
        if(request.user not in product.views.all()):
            transaction.on_commit(addView)
    return render(request,"product-detail.html",{"product":product,'boughted_by':boughted_by,"related":product_related, "title": product.name})


def AboutUS(request):
    products = Product.objects.filter(promoted=True)[:5]
    popular = Product.objects.all().annotate(count_views=models.Count("views")).order_by("-count_views")[:5]
    context = {
        "products":products,
        "popular":popular,
        "title": "About Us",
    }
    return render(request,"footer/about.html",context)

def Privacy(request):
    return render(request,"footer/privacy.html", {"title": "Privacy Policy"})

def Terms(request):
    return render(request,"footer/Terms.html", {"title": "Terms and Conditions"})