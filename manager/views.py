from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from store.models import Product,Payment,Image
from selltools.tools import getFilteredData
from store.models import Catagory
from users.models import User
from django.http.response import JsonResponse
from django.core.serializers import serialize
from .serializer import ProductSerailzer,ImageSerilizer
from django.contrib import messages
from .utils import Compare_return_compared_result
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum,Q,F
import json
import time

@login_required
def adminhome(request):
    product = Compare_return_compared_result(Product.objects)
    orders = Compare_return_compared_result(Payment.objects.filter(status="success"))
    users = Compare_return_compared_result(User.objects.filter(is_superuser=False),model="user")
    today = timezone.now().date()
    if(request.GET.get("month")):
        pass
    else:
        start_date = today - timedelta(days=30)
        successful_payments = Payment.objects.filter(status="success", date__gte=start_date).select_related('product')
    previous_month_start = start_date - timedelta(days=30)
    previous_month_payments = Payment.objects.filter(status="success", date__gte=previous_month_start, date__lt=start_date)
    
    sales_data = {}
    # Initialize last 30 days with 0
    for i in range(31):
        day = start_date + timedelta(days=i)
        sales_data[day.strftime('%Y, %b %d')] = 0

    for payment in successful_payments:
        date_str = payment.date.strftime('%Y, %b %d')
        if date_str in sales_data:
            sales_data[date_str] += payment.quantity * payment.product.price

    chart_labels = list(sales_data.keys())
    chart_values = list(sales_data.values())
    chart_labels = [chart_labels[i] if i in [0,3,6,9,12,15,18,21,24,27,30] else "" for i in range(len(chart_labels))]
    # Revenue Calculation
    # -----------------------------------------------
    total_revenue = 0
    for p in Payment.objects.filter(status="success"):
        total_revenue += p.quantity * p.product.price
    # Currrent Month Revenue
    current_month_revenue = 0
    for p in successful_payments:
        current_month_revenue += p.quantity * p.product.price
    # Previous Month Revenue
    previous_month_revenue = 0
    for p in previous_month_payments:
        previous_month_revenue += p.quantity * p.product.price
    # Revenue change Calculation
    revenue_growth = int((current_month_revenue - previous_month_revenue)) 

    # Graph Trend Calculation
    first_half_sum = sum(chart_values[:15])
    second_half_sum = sum(chart_values[-15:])
    
    if first_half_sum == 0:
        if second_half_sum > 0:
            graph_trend_percentage = 100
        else:
            graph_trend_percentage = 0
    else:
        graph_trend_percentage = int(((second_half_sum - first_half_sum) / first_half_sum) * 100)

    # Most Popular Product Calculation
    popular_product_data = Payment.objects.filter(status="success").values('product').annotate(total_qty=Sum('quantity')).order_by('-total_qty')
    
    popular_products = []
    
    if popular_product_data:
        for i in popular_product_data:
            popular_products.append({"product":Product.objects.get(pk=i['product']),"quantity":i['total_qty']})

    # Recent Orders
    recent_orders = Payment.objects.all().annotate(total_price=F('quantity') * F('product__price')).order_by('-date')[:5]

    return render(request,"dashboard.html",{'products':product,"orders":orders,"users":users, 'chart_labels': json.dumps(chart_labels), 'chart_values': json.dumps(chart_values), 'total_revenue': current_month_revenue, 'revenue_growth': revenue_growth, 'graph_trend_percentage': graph_trend_percentage, 'popular_products': popular_products, 'recent_orders': recent_orders, "title": "Dashboard"})
@login_required
def admin_product(request):
    products = Product.objects.all().order_by("-id")
    get_filtered_data = getFilteredData(products, request)
    return render(request,"manager_home.html",{"products":get_filtered_data[:100], "title": "Product Management"})

@login_required
def create_product(request):
    catagories = Catagory.objects.all()
    data = serialize("json",catagories)
    if(request.method == "POST"):
        img = ImageSerilizer(data=request.FILES)
        print(request.POST.get("product_images"))
        obj = ProductSerailzer(data=request.POST)
        if(obj.is_valid()):
            saved = obj.save()
            img.initial_data['product'] = saved.pk
            img.is_valid()
            img.save()
            return JsonResponse(data={"created":True})
        messages.error(request,"the Information you provided is incorrect")
    return render(request,"create_product.html",{"catagories":data,'home':reverse("admin_product"), "title": "Create Product"})    


def OrderView(request):
    objs = Payment.objects.all().order_by("-date")
    
    # Filter by status
    status = request.GET.get('status')
    if status and status != 'all':
        objs = objs.filter(status=status)
    elif not status: # Default to success if no status specified
         objs = objs.filter(status='success')

    # Search
    search = request.GET.get('search')
    if search:
        from django.db.models import Q
        objs = objs.filter(Q(product__name__icontains=search) | Q(user__name__icontains=search))

    # Date Range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        objs = objs.filter(date__gte=date_from)
    if date_to:
        objs = objs.filter(date__lte=date_to)

    return render(request,'order.html',{'orders':objs, "title": "Order Management"})


@login_required
def change_promote_status(request,id):
    product = Product.objects.get(id=int(id))
    product.promoted = not product.promoted 
    product.save()
    return redirect(reverse("admin_product"))

@login_required
def update_product(request,id):
    time.sleep(3)
    if(not request.user.is_superuser):
        return redirect(reverse("adminhome"))
    product = Product.objects.get(id=int(id))
    product_catagories = serialize("json",product.catagory.all())
    catagories = serialize("json",Catagory.objects.filter(~Q(id__in=product.catagory.all())))
    if request.method == "POST":
        try:
            # Update basic fields
            product.name = request.POST.get('product_name')
            product.about = request.POST.get('product_about')
            product.price = request.POST.get('product_price')
            product.weight = request.POST.get('product_weight')
            product.quantity = request.POST.get('product_quantity')
            
            # Update Detail
            detail_json = request.POST.get('product_detail')
            if detail_json:
                product.detail = json.loads(detail_json)
            
            # Update Categories
            cat_ids = request.POST.getlist('product_catagory')
            if cat_ids:
                # If cat_ids contains empty string (default), filter it out
                cat_ids = [c for c in cat_ids if c]
                if cat_ids:
                    product.catagory.set(cat_ids)
                else:
                    product.catagory.clear()
            else:
                product.catagory.clear()

            # Update Images
            # 1. Handle existing images (keep only those in existing_images list)
            existing_ids_json = request.POST.get('existing_images')
            if existing_ids_json:
                existing_ids = json.loads(existing_ids_json)
                product.images.exclude(id__in=existing_ids).delete()
            else:
                # If no existing_images sent, maybe delete all? 
                # Or if the field is missing, assume no changes to existing?
                # Better to be explicit. If empty list sent, delete all.
                # If not sent, maybe keep all? 
                # The frontend should send the list of IDs to keep.
                pass

            # 2. Add new images
            new_images = request.FILES.getlist('product_images')
            for img_file in new_images:
                Image.objects.create(product=product, img=img_file)

            product.save()
            return JsonResponse(data={"created":True})
        except Exception as e:
            print(e)
            return JsonResponse(data={"created":False, "error": str(e)}, status=400)

    return render(request,"update_product.html",{"product":product,"product_catagory":product_catagories,"catagories":catagories,'home':reverse("admin_product"), "title": "Update Product"})

@login_required
def customer_list(request):
    users = User.objects.filter(is_superuser=False).order_by("-created")
    return render(request, "customers.html", {"users": users, "title": "Customers"})

@login_required
def customer_detail(request, id):
    user = User.objects.get(id=id)
    orders = Payment.objects.filter(user=user).annotate(total_price=F('quantity') * F('product__price')).order_by("-date")
    return render(request, "customer_detail.html", {"c_user": user, "orders": orders, "title": "Customer Detail"})

@login_required
def delivery_list(request):
    # Filter for successful payments with delivery requested
    deliveries = Payment.objects.filter(status="success", delivery_on=True).order_by("-date")

    # Search
    search = request.GET.get('search')
    if search:
        deliveries = deliveries.filter(Q(product__name__icontains=search) | Q(user__name__icontains=search))

    # Date Range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        deliveries = deliveries.filter(date__gte=date_from)
    if date_to:
        deliveries = deliveries.filter(date__lte=date_to)

    return render(request, "delivery_list.html", {"deliveries": deliveries, "title": "Delivery Management"})
