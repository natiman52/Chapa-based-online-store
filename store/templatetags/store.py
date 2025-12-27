from django import template
register = template.Library()

@register.filter
def find_rated(ratings,user):
    return ratings.filter(user=user)
@register.filter
def get_sort(value):
    try:
        search_query= value.get_full_path().split("?")[1]
    except:
        search_query=""
    sort = value.GET.get("sort")
    q = value.GET.get("price_range")  
    test = 0
    print(search_query)
    for i in ["sort","page","search","price_range"]:
        if(i in search_query):
            test += 1
    if(test == 4):
        return f"&sort={sort}&price_range={q}&page={ value.GET.get("page")}&search={value.GET.get("search")}" 
    elif("price_range" in search_query):
        return f"&price_range={q}"
    elif("page" in search_query):
        return f"&page={ value.GET.get("page")}"
    elif("search" in search_query):
        return f"&search={value.GET.get("search")}"
    else:
        return ""
    
@register.filter
def get_total_star(val,cou):
    total = 0
    for v in val:
        total += v.rate
    if(cou != 0):
        avg = total / cou
    else:
        avg = total
    return round(avg)


@register.filter
def get_range(val):
    return range(val)



@register.filter
def find_if_exists(item,cart_items):
    test = cart_items.filter(product=item)
    if(test.exists()):
        return True
    return False

@register.filter
def multibyone(value):
    return value * -1

@register.filter
def mul(value,p):
    return value * p

@register.filter
def checklength(value):
    result = value if len(value) < 20 else f"{''.join(list(value)[0:15])}..."
    return result