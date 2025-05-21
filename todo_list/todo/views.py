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
                # Set session using email
                request.session['email'] = check.first().email
                return render(request, 'login.html', {
                    'success': 'Login successful! Redirecting to your tasks...',
                    'redirect': True
                })
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'login.html', {'error': 'Missing email or password'})

    return render(request, 'login.html')

def tasks(request):
    # Only show tasks for the logged-in user
    if 'email' in request.session:
        user_email = request.session['email']
        userid = user.objects.get(email=user_email)
        tasks_list = task.objects.filter(user=userid)
        return render(request, 'tasks.html', {'tasks': tasks_list})
    else:
        return HttpResponse('User not logged in')

def todo(request):
    if request.method == 'POST':
        if 'email' in request.session:
            user_email = request.session['email']
            print("User email from session:", user_email)
            try:
                userid = user.objects.get(email=user_email)
            except user.DoesNotExist:
                return HttpResponse('User not found')
            task_title = request.POST.get('task')
            print("Task title from form:", task_title)
            if task_title:
                taskdetails = task.objects.create(user=userid, title=task_title)
                print("Task created:", taskdetails)
                # Show updated tasks list
                tasks_list = task.objects.filter(user=userid)
                return render(request, 'tasks.html', {'tasks': tasks_list})
            else:
                return HttpResponse('Task title is required')
        else:
            return HttpResponse('User not logged in')
    return HttpResponse('Invalid Method')
