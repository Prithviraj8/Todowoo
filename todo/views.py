from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):

    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        # Create a new user object
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) # 'username' & 'password1' are names of the username and password text fields.
                # You can click inspect on chrome and get these names from the HTML code displayed on the console.   
                user.save()
                login(request, user)
                return redirect('currentTodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html',{'form': UserCreationForm(), 'error': 'Username already in use'})                                                                          


        else:
            # Tell the user that the passwords didn't match.
            print ("Mismatched passwords")    
            return render(request, 'todo/signupuser.html',{'form': UserCreationForm(), 'error': 'Passwords did not match'})                                                                          

def loginuser(request):

    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username= request.POST['username'], password= request.POST['password'])      
        if user is not None:
            login(request, user)
            return redirect('currentTodos')
        else:
            return render(request, 'todo/loginuser.html', {'error':'Username or password are incorrect'})




def logoutuser(request):
    if request.method == 'POST':
        print("REQ ", request.POST)
        logout(request)

        return redirect('home')


def currentTodos(request):
    return render(request, 'todo/currentTodos.html')