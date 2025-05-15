from django.shortcuts import render,HttpResponse
from .models import *

# Create your views here.

def open(request):
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Password = request.POST.get('pass')

        if Name and Email and Password:
            # Check if user already exists
            if user.objects.filter(email=Email).exists():
                return HttpResponse('Email already registered')
            data = user.objects.create(name=Name, email=Email, password=Password)
            data.save()
            return render(request, 'login.html', {'message': 'Registration successful. Please log in.'})
        else:
            return render(request, 'register.html', {'error': 'All fields are required.'})

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        Password = request.POST.get('pass')
        
        if Email and Password:
            check = user.objects.filter(email=Email, password=Password)
            if check.exists():
                return HttpResponse('Account Exists')
            else:
                return HttpResponse('Invalid credentials')
        else:
            return HttpResponse('Missing email or password')

    #return render(request, 'login.html')
    return HttpResponse('Failed')
