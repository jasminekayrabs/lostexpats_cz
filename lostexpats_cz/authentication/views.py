from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 

# Create your views here.
#Taking user input on the back-end and saving it to the database
def home(request):
    return render(request, "authentication/index.html")

def render_signup(request):
    if request.method == "POST":
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['pass1']
        confpassword = request.POST['pass2']
#to create a user
        myuser = User.objects.create_user(firstname, email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname 

        myuser.save()
#printing succeful signup message
        messages.success(request, "Your account has been created.")

#redirecting user to login
        return redirect('render_login')
    return render(request, "authentication/signup.html")

def render_login(request):
    return render(request, "authentication/login.html")

def render_logout(request):
    pass
