# middleware.py
from django.shortcuts import redirect

class UserUUIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logic to check for user UUID in POST request
        if request.method == 'POST' and 'submit_user_uuid' in request.POST:
            user_UUID = request.POST.get('user_UUID')
            if user_UUID:
                return redirect('cart-items', user_UUID)
        
        # Proceed with the response if no UUID logic is triggered
        response = self.get_response(request)
        return response


