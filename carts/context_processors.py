from .models import Cart,CartItem
from .views import _get_cart_id

def counter(request):
    cart_count=0

    try: #### NOTA erro de AnonimousUser is not iterable, al usar --> request.user
        if request.user.is_authenticated:
            cart=Cart.objects.filter(user=request.user)#cart_id=_get_cart_id(request)
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
        # Variable global que es cart_count para ser usada en mi templates
    return dict(cart_count=cart_count)