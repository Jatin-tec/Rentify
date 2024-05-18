from django.shortcuts import render
from authentication.models import Profile
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = Profile.objects.filter(email=email).first()
        if  user:
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                messages.success(request, 'Login successful')
                return render(request, 'dashboard.html')
            else:
                messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    # Redirect to a success page, or wherever you want the user to go after logout
    return redirect('home') 

def register(request):
    if request.method == 'POST':
        try:
            # Create a new user
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            phone = request.POST.get('phone', None)
            email = request.POST.get('email', None)
            password = request.POST.get('password', None)
            
            # Save the user to the database
            user = Profile(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                email=email
            )
            user.set_password(password)
            user.save()
            messages.success(request, 'User created successfully')
            return render(request, 'login.html')
        except Exception as e:
            messages.error(request, f'An error occurred while creating the user: {e}')
            return render(request, 'signup.html')
    return render(request, 'signup.html')