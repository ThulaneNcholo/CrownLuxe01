from django.shortcuts import render,redirect
from products.models import *
import random

# models import 
from .models import *
from cart.models import *

# Create your views here.
def IndexView(request):
    catalog = ProductCatalogModel.objects.all()
    best_selling = ProductModel.objects.filter(best_sellers = True)[:4]
    product_item = ProductModel.objects.order_by('?').first()

    # Add Product Item to Cart Function
    if request.method == 'POST' and 'submit_product_item' in request.POST:
        product_id = request.POST.get('product_id')
        product_selected = ProductModel.objects.get(id = product_id)
        current_user = request.POST.get('user_ID')

        add_to_cart = CartItemsModel()
        add_to_cart.reference = random.randrange(0, 10000000)
        add_to_cart.current_user = current_user
        add_to_cart.product = product_selected
        add_to_cart.quantity = 1
        add_to_cart.total = product_selected.price
        add_to_cart.save()
        return redirect('cart-items',current_user )

    context = {
        "catalog" : catalog,
        "best_selling" : best_selling,
        "product_item" : product_item
    }

    return render(request,'client/index.html',context)


def ContactUsView(request):
    return render(request,'client/contact.html')

def CatalogListView(request,id):
    catalog = ProductCatalogModel.objects.get(id = id)
    catalogItems = ProductModel.objects.filter(product_catalog = catalog)

    context = {
        "catalog" : catalog,
        "catalogItems" : catalogItems
    }

    return render(request,'client/catalog_list.html',context)

def ReviewsView(request):
    reviews = ReviewsModel.objects.all()

    # Add Review post method
    if request.method == 'POST' and 'submit_review' in request.POST:
        add_review = ReviewsModel()
        add_review.FirstName = request.POST.get('FirstName')
        add_review.LastName = request.POST.get('LastName')
        add_review.Review = request.POST.get('review')
        add_review.rating = request.POST.get('rating')
        add_review.save()
        return redirect('our-reviews')
    
    context = {
        "reviews" : reviews
    }
    

    return render(request,'client/reviews.html',context)

