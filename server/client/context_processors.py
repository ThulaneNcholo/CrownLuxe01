from cart.models import CartItemsModel

# context_processors.py
def user_uuid_context_processor(request):
    if request.method == 'POST' and 'submit_user_uuid' in request.POST:
        user_UUID = request.POST.get('user_UUID')
        if user_UUID:
            # Redirect if needed (though redirects are better in middleware)
            return {'user_UUID': user_UUID}
    return {}


