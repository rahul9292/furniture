from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Product, Order, OrderItem


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact.html')

def signup(request):
    return render(request, 'account/signup.html')




@login_required(login_url='account_login')
def view_cart(request):
    if Order.objects.filter(customer=request.user).exists():
        messages.info(request, "You have already placed an order. You cannot access the cart until your order is delivered.")
        return redirect('latest_order_detail')

    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'total': float(item_total),
            'image': product.image.url if product.image else None,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required(login_url='signup')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] < 10:
            cart[str(product_id)] += 1
        else:
            messages.warning(request, "Maximum quantity reached.")
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')


@login_required(login_url='signup')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')


@login_required(login_url='signup')
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('view_cart')


@login_required(login_url='signup')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Your cart is empty!")
        return redirect('view_cart')

    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'name': product.name,
            'quantity': quantity,
            'total': float(item_total),
        })

    return render(request, 'order.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required(login_url='signup')
def process_order(request):
    if request.method == "POST":
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        total_price = request.POST.get('total_price')

        if not (address and city and state and phone and total_price):
            messages.error(request, "Please fill in all required fields.")
            return redirect('view_cart')

        order = Order.objects.create(
            customer=request.user,
            address=address,
            city=city,
            state=state,
            phone=phone,
            total_price=total_price,
        )

        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        request.session['cart'] = {}
        request.session['order_placed'] = True
        request.session.modified = True

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_detail', order_id=order.id)

    return redirect('view_cart')


@staff_member_required
def admin_order_list(request):
    orders = Order.objects.prefetch_related('items__product').all().order_by('-id')
    return render(request, 'admin_orders.html', {'orders': orders})


@login_required(login_url='account_login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_items = order.items.select_related('product')
    return render(request, 'my_order.html', {
        'order': order,
        'order_items': order_items,
    })


@login_required(login_url='account_login')
def latest_order_detail(request):
    order = Order.objects.filter(customer=request.user).order_by('-created_at').first()
    if not order:
        messages.info(request, "You have no recent orders.")
        return redirect('home')
    return redirect('order_detail', order_id=order.id)


def search_results(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search.html', {'query': query, 'results': results})
