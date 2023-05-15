from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect

 
# Create your views here.
#render functions allow the pages to be run on the server
def home(request):
    return render(request, "authentication/index.html")

def render_fooddrinks(request):
    return render(request, "authentication/fooddrinks.html")

def render_nightlife(request):
    return render(request, "authentication/nightlife.html")

def render_news(request):
    return render(request, "authentication/news.html")


#Taking user input on the back-end and saving it to the database
@csrf_protect
def render_signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        pass2 = request.POST['pass2']
#to create a user
        myuser = User.objects.create_user(fname, email,password)
        myuser.first_name = fname
        myuser.last_name = lname 

        myuser.save()
#printing succeful signup message
        messages.success(request, "Your account has been created.")
#redirecting user to login
        return redirect('render_login')

        # render the signup form
        return render(request, 'signup.html')

    return render(request, "authentication/signup.html")

#FOR LOGIN
def render_login(request):

    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']

        #authenticating user: return a none response if user is not authenticated
        # the authentication is also the sanitisation of user input. This will prevent SQL injections from being carried outsuccessfully.

        # The below code pulls the email and password from the POST request (user input through login form). Then, the authenticate function takes care of authenticating user credentials against an authentication back end, which,  is the database

        user = authenticate(email = email, password = pass1)

        #allow user to login if they are authenticated
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        #print error message if user is not authenticated
        else:
            messages.error(request, "Wrong email or password!")
            return redirect('home')

    return render(request, "authentication/login.html")

def render_logout(request):
    logout(request)
    messages.success(request, "looged out")
    return redirect('home')
