import random
import string
from django.shortcuts import redirect
from django.urls import reverse

DELIVERY_INITIAL = 100

def getDeliveryPrice(products,location):
    total = 0
    ## calcluate distance
    price = 0

    #calculate weight
    for i in products:
        print(i.weight)
        total += i.weight
    if(total > DELIVERY_INITIAL):
        price += 100
    total += price
    return total
def is_profile_complete(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.sociallogin:
            return redirect(reverse("account_finish")) 
        
        response = view_func(request, *args, **kwargs)
        
        # Add your custom logic here after the view function is called
        # Example: Modify the response
        # response['X-Custom-Header'] = 'Decorated!'
        
        return response
    return wrapper


def generate_random_lower_string():
    """
    Generates a random string of a specified length,
    containing uppercase letters, lowercase letters, and digits.
    """
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(characters) for i in range(50))
    return random_string


def generate_random_upper_string():
    """
    Generates a random string of a specified length,
    containing uppercase letters, lowercase letters, and digits.
    """
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for i in range(6))
    return random_string