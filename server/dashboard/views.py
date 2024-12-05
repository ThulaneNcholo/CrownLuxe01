from django.shortcuts import render,get_object_or_404, redirect
from cart.models import *
import os
from django.conf import settings

import uuid
from django.contrib import messages  

# Create your views here.
def DashboardView(request):
    orders = CustomerOrderModel.objects.all().order_by('-date_created')
    new_orders = CustomerOrderModel.objects.filter(status = 'Order')
    process_orders = CustomerOrderModel.objects.filter(status = 'processing')
    complete_orders = CustomerOrderModel.objects.filter(status = 'Complete')
    returned_orders = CustomerOrderModel.objects.filter(status = 'returned')

    # count status 
    all_orders = orders.count()
    orders_count = new_orders.count()
    complete_count = complete_orders.count()
    returned_count = returned_orders.count()
    processing_count = process_orders.count()

    # Increase Item Quantity
    if request.method == 'POST' and 'update_order' in request.POST:
        orderID = request.POST.get('orderID') 
        update_order = CustomerOrderModel.objects.get(id = orderID)
        update_order.status = request.POST.get('updatedStatus') 
        update_order.save()
        return redirect('dashboard')

    context = {
        "orders": orders,
        "new_orders" : new_orders,
        "process_orders" : process_orders,
        "complete_orders" : complete_orders,
        "returned_orders" : returned_orders,
        "all_orders" : all_orders,
        "complete_count" : complete_count,
        "returned_count" : returned_count,
        "processing_count" : processing_count,
        "orders_count" : orders_count
    }

    return render(request,'dashboard/dashboard.html',context)


def OrderViewAdmin(request,id):
    order = CustomerOrderModel.objects.get(id = id)
    order_items = order.customer_items.all()

     # Create a list of dictionaries
    order_status = [
        {"id": 1, "name": "Order"},
        {"id": 2, "name": "processing"},
        {"id": 3, "name": "Complete"},
        {"id": 4, "name": "returned"},
    ]

    total_qty = 0
    
    # items count 
    for i in order_items:
        count_qty = i.quantity + total_qty
        total_qty = count_qty

    total_qty

    # Increase Item Quantity
    if request.method == 'POST' and 'confirm_update' in request.POST:
        update_order = CustomerOrderModel.objects.get(id = id)
        update_order.status = request.POST.get('status_value')
        update_order.save()
        messages.success(request,'Order Updated') 
        return redirect('order-view', id)


    context = {
        "order" : order,
        "order_items" : order_items,
        "total_qty" : total_qty,
        "order_status" : order_status
    }

    return render(request,'dashboard/orderView_admin.html',context)


def AdminItemsView(request):
    products = ProductModel.objects.all().exclude(product_catalog = 4)
    accessories = ProductModel.objects.filter(product_catalog = 4)
    
    context = {
        "products" : products,
        "accessories" : accessories,
    }

    return render(request,'admin_items/admin_products.html',context)

def ViewProductAdminView(request,id):
    catalog = ProductCatalogModel.objects.all()
    product = ProductModel.objects.get(id = id)
    items = product.product_details.all()

    context = {
        "product" : product,
        "catalog" : catalog,
        "items" : items
    }
    return render(request,'dashboard/view_product_admin.html',context)

def AdminProductPartialView(request):
    return render(request,'partials/admin_product_partial.html')

def NewProductView(request,product_id=None):
    catalog = ProductCatalogModel.objects.all()
    items = request.session.get('items', [])

    if product_id:
        # Editing an existing product
        product = get_object_or_404(ProductModel, id=product_id)
    else:
        # Creating a new product
        product = None

    # Create New Product Post
    if request.method == 'POST' and 'submit_product' in request.POST:
        save_product = ProductModel()
        save_product.name = request.POST.get('productName')
        save_product.price = request.POST.get('price')
        save_product.description = request.POST.get('description')
        save_product.cover_image = request.FILES.get('coverImage', None)
        save_product.image1 = request.FILES.get('image2', None)
        save_product.image2 = request.FILES.get('image3', None)
        best_sellers = request.POST.get('bestSellers')

        if best_sellers:
            save_product.best_sellers = best_sellers
        
        # product catalog 
        catalog_id = request.POST.get('product_catalog')
        if catalog_id:
            catalog_object = ProductCatalogModel.objects.get(id = catalog_id)
            # continue to save product 
            save_product.product_catalog = catalog_object
        save_product.save()

        for i in items:
            create_item = ProductDetailsModel()
            create_item.title = i['type']
            create_item.description = i['detailsDescription']
            create_item.save()
            save_product.product_details.add(create_item)

        # update session to be clear 
        if 'items' in request.session:
            del request.session['items']

        return redirect('product_edit',save_product.id)
    

    # update Product
    if request.method == 'POST' and 'edit_product' in request.POST:
        print('updated top')
        edit_product = ProductModel.objects.get(id = product_id)
        edit_product.name = request.POST.get('productName')
        edit_product.price = request.POST.get('price')
        edit_product.description = request.POST.get('description')
        # product catalog 
        catalog_id = request.POST.get('product_catalog')
        catalog_object = ProductCatalogModel.objects.get(id = catalog_id)
        # continue to save product 
        edit_product.product_catalog = catalog_object

        # update best seller option boolean if updated 
        bestSellers = request.POST.get('bestSellers')
        if bestSellers:
            edit_product.best_sellers = bestSellers

        # Check if images have been changed; if not, keep the uploaded one
        image_mappings = {
            'cover_image': 'coverImage',
            'image1': 'image2',
            'image2': 'image3',
        }

        for field, file_key in image_mappings.items():
            new_image = request.FILES.get(file_key, None)
            if new_image:
                # Delete the old image if it exists
                old_image = getattr(edit_product, field, None)
                if old_image and old_image.name:  # Check if the field has an old image
                    old_image_path = os.path.join(settings.MEDIA_ROOT, old_image.name)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # Assign the new image
                setattr(edit_product, field, new_image)

        edit_product.save()

        for i in items:
            print(i['type'])
            create_item = ProductDetailsModel()
            create_item.title = i['type']
            create_item.description = i['detailsDescription']
            create_item.save()
            edit_product.product_details.add(create_item)

        # update session to be clear 
        if 'items' in request.session:
            del request.session['items']

        messages.success(request,'Item Updated') 
        return redirect('product_edit',product_id)
    
    # Delete Product
    if request.method == 'POST' and 'delete_product' in request.POST:
        product = ProductModel.objects.get(id=product_id)
        # Delete related product details
        product.product_details.clear()
        # Delete images
        product.cover_image.delete()
        product.image1.delete()
        product.image2.delete()
        # Delete the product itself
        product.delete()
        
        return redirect('admin-products')

    context = {
        "catalog" : catalog,
        "items" : items,
        "product" : product,
    }

    return render(request,'admin_items/new_product.html',context)


# htmx Views 
def ProductDetailsPartialView(request):
    items = request.session.get('items', [])

    if request.method == 'POST':
        type = request.POST.get('type')
        detailsDescription = request.POST.get('detailsDescription')

        # Generate a unique ID for the item
        item_id = str(uuid.uuid4())

         # Create a dictionary from the POST data
        item = {
            "id": item_id,
            "type": type,
            "detailsDescription": detailsDescription,
        }

        # Retrieve the existing session data or initialize an empty list
        items_list = request.session.get('items', [])

        # Append the new dictionary to the list
        items_list.append(item)

        # Save the updated list back to the session
        request.session['items'] = items_list

        # Retrieve the list of dictionaries from the session
        items = request.session.get('items', [])

    items = request.session.get('items', [])

    context = {
        "items": items
    }

    return render(request,'partials/product_partial.html',context)


# htmx delete session item 
def RemoveItemSessionView(request):
    items = request.session.get('items', [])

    if request.method == 'POST':
        # Retrieve the ID of the item to remove
        item_id = request.POST.get('item_id')

        # Retrieve the session data (list of dictionaries)
        items_list = request.session.get('items', [])

        # Filter out the item with the matching ID
        updated_list = [item for item in items_list if item.get('id') != item_id]

        # Update the session with the modified list
        request.session['items'] = updated_list

    items = request.session.get('items', [])

    context = {
        "items": items
    }

    return render(request,'partials/product_partial.html',context )

# htmx delete item from object 
def RemoveMainProductDetailsView(request,id):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        remove_item = ProductDetailsModel.objects.get(id = item_id)
        remove_item.delete()
        remove_item.save()
        product = get_object_or_404(ProductModel, id=id)

        context = {
            "product" : product
        }

    
    return render(request,'partials/admin_product_partial.html',context)


