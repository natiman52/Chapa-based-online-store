from django.contrib.sitemaps import Sitemap
from store.models import Product,Catagory
from django.urls import reverse
from faq.models import Question
from django.db.models import Q

def getFilteredData(products,request):
    result = products
    if(request.GET.get("catagory") and request.GET.get("catagory") != ""):
        result = products.filter(catagory__name=request.GET.get("catagory"))
    if(request.GET.get("price_in") and request.GET.get("price_out") and request.GET.get("price_in") != "" and request.GET.get("price_out") != ""):
        result = result.filter(price__range=[int(request.GET.get("price_in")),int(request.GET.get("price_out"))])
    elif(request.GET.get("price_in") and request.GET.get("price_in") != ""):
        result = result.filter(price__gte=int(request.GET.get("price_in")))
    elif(request.GET.get("price_out") and request.GET.get("price_out") != ""):
        result = result.filter(price__lte=int(request.GET.get("price_out")))
    if(request.GET.get("weight") and request.GET.get("weight") != ""):
        result = result.filter(weight__lte=int(request.GET.get("weight")))
    if(request.GET.get("search") and request.GET.get("search") != ""):
        result = result.filter(Q(name__icontains=request.GET.get("search")) | Q(about__icontains=request.GET.get("search")) | Q(catagory__name__icontains=request.GET.get("search")))
    if(request.GET.get("promoted") and request.GET.get("promoted") == "Promoted"):
        result = result.filter(promoted=True)
    elif(request.GET.get("promoted") and request.GET.get("promoted") == "Unpromoted"):
        result = result.filter(promoted=False)
    return result
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return f"/product/{obj.id}"
    

class CatagorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Catagory.objects.all()

    def location(self, obj):
        return f"/catagory/{obj.name}"
 
class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = "weekly"

    def items(self):
        return ["home", "about", "terms","privacy","faq:index_view"]

    def location(self, item):
        return reverse(item)
    

class QuestionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Question.objects.all()

    def location(self, obj):
        return reverse("faq:question_detail", args=[obj.slug])
 