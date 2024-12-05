from django.shortcuts import render,redirect
from .models import *
import random

from decimal import Decimal
from django.db.models import Sum
from django.db.models import Q

# Create your views here.
def CartView(request,id):
    currentUser_items = CartItemsModel.objects.filter(Q(current_user = id) & Q(status = "InCart"))
    current_user_uuid = id

    # Sum the total_price from each item in the cart
    total_price = currentUser_items.aggregate(total=Sum('total'))['total'] or Decimal(0)

    # Increase Item Quantity
    if request.method == 'POST' and 'IncreaseQty' in request.POST:
        item_ID = request.POST.get('item_ID')
        cart_product = CartItemsModel.objects.get(id = item_ID)
        product_quantity = cart_product.quantity
        product_total = cart_product.total
        cart_product.quantity = product_quantity + 1
        cart_product.total = float(product_total) + float(cart_product.product.price)
        cart_product.save()
        return redirect('cart-items',id)
    
    # Decrease Item Quantity
    if request.method == 'POST' and 'decreaseQty' in request.POST:
        item_ID = request.POST.get('item_ID')
        cart_product = CartItemsModel.objects.get(id = item_ID)
        product_quantity = cart_product.quantity
        product_total = cart_product.total
        cart_product.quantity = product_quantity - 1
        cart_product.total = float(product_total) - float(cart_product.product.price)
        cart_product.save()

        if cart_product.quantity == 0:
            cart_product = CartItemsModel.objects.get(id = item_ID)
            cart_product.delete()
            
        return redirect('cart-items',id)

    context = {
        "currentUser_items" : currentUser_items,
        "total_price" : total_price,
        "current_user_uuid" : current_user_uuid
    }

    return render(request,'cart/cart_view.html',context)

def CustomerContactView(request,id):
    currentUser_items = CartItemsModel.objects.filter(Q(current_user = id) & Q(status = "InCart"))
    # Sum the total_price from each item in the cart
    total_price = currentUser_items.aggregate(total=Sum('total'))['total'] or Decimal(0)

    # Decrease Item Quantity
    if request.method == 'POST' and 'submit_contact_details' in request.POST:
        # Create Customer Order 
        create_order = CustomerOrderModel()
        create_order.reference = random.randrange(0, 10000000)
        create_order.current_user = id
        create_order.full_name = request.POST.get('fullName')
        create_order.email = request.POST.get('email')
        create_order.phone_number = request.POST.get('phoneNumber')
        create_order.street = request.POST.get('street')
        create_order.city = request.POST.get('city')
        create_order.province = request.POST.get('province')
        create_order.postal_code = request.POST.get('postal_code')
        create_order.total = total_price
        create_order.save() 
        # save user id to django session 
        request.session['current_user'] = create_order.current_user 
        request.session['current_order'] = create_order.id 

        # update many to many product field 
        for item in currentUser_items:
            cart_item = CartItemsModel.objects.get(id = item.id)
            create_order.customer_items.add(cart_item)
            create_order.save()

        
            
        return redirect("Payments-view", create_order.id)

    context = {
        "total_price" : total_price
    }

    return render(request,'cart/customer_contact.html',context)

def PaymentSuccessfulView(request):
    current_user_id = request.session.get('current_user')
    current_order_id = request.session.get('current_order')
    
    # update customer order when payment is complete 
    update_order = CustomerOrderModel.objects.get(id = current_order_id)
    update_order.status = "Order"
    update_order.save()

    # Filter and bulk update the status to 'Order'
    CartItemsModel.objects.filter(
        Q(current_user=current_user_id) & Q(status="InCart")
    ).update(status="Order") 

    return render(request,'cart/payment_success.html')
