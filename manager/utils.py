from django.utils import timezone


def Compare_return_compared_result(obj,model='products'):
    past_month = timezone.datetime.today() - timezone.timedelta(days=30)
    if(model !="user"):
        past_objs = obj.filter(date__lt=past_month)
        current_objs = obj.filter(date__gte=past_month)
    else:
        past_objs = obj.filter(created__date__lt=past_month)
        current_objs = obj.filter(created__date__gte=past_month)
    try:
        percentage_diff = (current_objs.count() - past_objs.count()) / past_objs.count()
        percentage_diff = int(percentage_diff * 100)
    except:
        percentage_diff = (current_objs.count() - past_objs.count()) / 1
        percentage_diff = int(percentage_diff * 100)
    return {"total":obj.all(),"past_objs":past_objs,"current_objs":current_objs,"percentage_diff":abs(percentage_diff),'growth':percentage_diff}
    
