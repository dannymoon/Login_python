from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def success(request):
    return render(request, 'login/success.html')

def login(request):
    if request.method == 'POST':
        if not 'login_status' in request.session:
            request.session['login_status'] = False
        login_data = User.objects.filter(email=request.POST['email'])
        if len(request.POST['email']) < 1:
            messages.error(request, "enter email")
            return redirect('/')
        if len(request.POST['password']) < 1:
            messages.error(request, "enter password")
            return redirect('/')
        inputted_password = request.POST['password']
        stored_password = User.objects.filter(email=request.POST['email']).first().password

        if login_data and bcrypt.checkpw(inputted_password.encode(), stored_password.encode()):
            request.session['login_status'] = {'id':login_data.first().id, 'first_name':login_data.first().first_name, 'last_name':login_data.first().last_name, 'email':login_data.first().email}
            return redirect('/success')
        else:
            messages.error(request, "Email and password does not match")
            return redirect('/')
    

def process(request):
    if request.method == 'POST':
        
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/')
        else:
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
            messages.error(request, "Successfully Registered!")
            return redirect('/success')