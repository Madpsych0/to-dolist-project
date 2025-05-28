from django.shortcuts import render, HttpResponse, redirect
from .models import *
import re
from django.contrib import messages

# Create your views here.

def open(request):
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Password = request.POST.get('pass')

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if Name and Email and Password:
            if not re.match(pattern, Password):
                return render(request, 'register.html', {
                    'error': 'Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.'
                })
            if user.objects.filter(email=Email).exists():
                return render(request, 'register.html', {'error': 'Email already exists.'})
            data = user.objects.create(name=Name, email=Email, password=Password)
            data.save()
            return render(request, 'register.html', {
                'success': 'Registration successful! Please login.',
                'redirect': True
            })
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
                return render(request, 'tasks.html', {'error': 'Task title is required'})
        else:
            return HttpResponse('User not logged in')
    return HttpResponse('Invalid Method')

def mark_done(request, task_id):
    if 'email' in request.session:
        try:
            t = task.objects.get(id=task_id, user__email=request.session['email'])
            t.completed = not t.completed
            t.save()
        except task.DoesNotExist:
            pass
    return redirect('task')

def delete_task(request, task_id):
    if 'email' in request.session:
        try:
            t = task.objects.get(id=task_id, user__email=request.session['email'])
            t.delete()
        except task.DoesNotExist:
            pass
    return redirect('task')

def logout(request):
    if 'email' in request.session:
        request.session.flush()
        messages.success(request, 'You have been logged out.')
        return redirect('login')
    messages.error(request, 'Your Session Time has Expired. Please Login Again')
    return redirect('login')
