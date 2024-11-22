from django.shortcuts import render,redirect
import random

# Models Import 
from .models import *
from cart.models import * 


# Create your views here.
def AllProductsView(request):
    products = ProductModel.objects.all()

    context = {
        "products" : products
    }

    return render(request,'products/products_all.html',context)

def ProductView(request,id):
    product = ProductModel.objects.get(id = id)
    product_details = product.product_details.all()
    similar_products = ProductModel.objects.all().exclude(id = id).order_by('?')[:3]

    # Add to cart
    if request.method == 'POST' and 'add_to_cart' in request.POST:
        quantity = request.POST.get('inputQty')
        product_price = float(product.price) * float(quantity)
        current_user = request.POST.get('current_user')

        add_cart = CartItemsModel()
        add_cart.reference = random.randrange(0, 10000000)
        add_cart.current_user = current_user
        add_cart.product = product
        add_cart.quantity = quantity
        add_cart.total = product_price
        add_cart.save()
        return redirect('cart-items',current_user)

    context = {
        "product" : product,
        "product_details" : product_details,
        "similar_products" : similar_products
    }

    return render(request,'products/product_view.html',context)
