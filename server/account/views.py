from django.shortcuts import render,redirect
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
@unauthenticated_user
def LoginPageView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('login')

    return render(request,'account/login.html')

# logout user 
def LogoutUser(request):
    logout(request)
    return redirect('login')