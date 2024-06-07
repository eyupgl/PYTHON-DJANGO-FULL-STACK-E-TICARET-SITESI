# store/views.py
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})
@login_required(login_url="user:login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    cart = request.session.get('cart', {})

    cart_item = cart.get(str(product_id))
    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart_item = {
            'product_id': product_id,
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else ''
        }
    cart[str(product_id)] = cart_item

    request.session['cart'] = cart

    return redirect('cart_view')

@login_required(login_url="user:login")
def cart_view(request):
    cart = request.session.get('cart', {})
    
    total_price = 0
    for item in cart.values():
        total_price += float(item['price']) * item['quantity']

    return render(request, 'store/cart.html', {'cart': cart, 'total_price': total_price})
def remove_from_cart(request, item_id):
    # Sepetteki ürünü kaldır
    if 'cart' in request.session:
        cart = request.session['cart']
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart
    return redirect('cart_view')

def added_products(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})