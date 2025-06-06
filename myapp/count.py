from .models import Order

def order_count(request):
    count = 0
    if request.user.is_authenticated:
        if request.user.is_staff:
            count = Order.objects.filter(is_delivered=False).count()
        else:
            count = Order.objects.filter(customer=request.user, is_delivered=False).count()
    return {'order_count': count}