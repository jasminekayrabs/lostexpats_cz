from django.shortcuts import render

# Create your views here.
#Taking user input on the back-end and saving it to the database
def home(request):
    return render(request, "authentication/index.html")

def render_signup(request):
    return render(request, "authentication/signup.html")

def render_login(request):
    return render(request, "authentication/login.html")

def render_logout(request):
    pass
