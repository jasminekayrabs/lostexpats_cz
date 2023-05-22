from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.views.generic import TemplateView



#render functions allow the pages to be run on the server
def home(request):
     return render(request, "authentication/index.html")

def render_fooddrinks(request):
    return render(request, "authentication/fooddrinks.html")

def render_nightlife(request):
    return render(request, "authentication/nightlife.html")

def render_news(request):
    return render(request, "authentication/news.html")

def render_events(request):
    return render(request, "authentication/events.html")




#FOR SIGNUP
# By adding csrf_protect here and %csrf_token% in .html files, Django will automatically generate and validate CSRF tokens for each form submission. The CSRF token will be included in the form submission and verified on the server-side, protecting against CSRF attacks.

# By applying the escape function to the user-generated input, you ensure that any HTML tags or special characters are properly escaped and treated as plain text.

@csrf_protect
def render_signup(request):
    if request.method == "POST":
        fname = escape(request.POST['fname'])
        lname = escape(request.POST['lname'])
        email = escape(request.POST['email'])
        password = request.POST['pass1']
        pass2 = request.POST['pass2']
#to create a user
        myuser = User.objects.create_user(fname, email,password)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.save()

        return redirect('render_login')
    return render(request, "authentication/signup.html")


# #FOR LOGIN
#  the escape function is applied to the email and pass1 variables to ensure that any user-generated content is properly escaped and treated as plain text. This helps protect against potential XSS attacks.
@csrf_protect
def render_login(request):
     # Retrieve success message from query parameters
    success_message = request.GET.get('success_message')
    if request.method == "POST":
        email = escape(request.POST['email'])
        pass1 = escape(request.POST['pass1'])

# The 'authenticate' function in Django is used for user authentication. It takes in a set of credentials (in this case email and password) and verifies whether they correspond to a valid user in the system. It enhances the security of the authentication process by verifying user credentials and protecting against common attack vectors. The function returns a user object if the authentication is successful or None if the authentication fails.

# It ensures that the provided credentials match a valid user in the system, thereby protecting against credential stuffing attacks, where attackers use a list of stolen username/password combinations to gain unauthorized access.

# The authenticate function handles user authentication securely by using parameterized queries and prepared statements, which effectively prevent SQL INJECTION attacks. It ensures that user input is properly escaped and sanitized before being used in database queries.

# The below code pulls the email and password from the POST request (user input through login form). Then, the authenticate function takes care of authenticating user credentials against the authentication back end.
 
        ## Use parameterized queries to protect against SQL injection
        user = authenticate(request, email = email, password = pass1)

        
        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        else:
            # User authentication failed, display error message
            messages.error(request, "Wrong email or password!")
            return redirect('home')
    
    email = escape(request.POST.get('email', ''))
    return render(request, "authentication/login.html")

#FOR LOGOUT
def render_logout(request):
    logout(request)
    messages.success(request, "logged out")
    return redirect('home')

#Session cookies
def index(request):
     # Create an HTTP response with the message "Welcome to the landing page!"
     response = HttpResponse("Welcome to the landing page!")

     # Set a cookie named "my_cookie" with a value of "cookie_value"
     response.set_cookie('my_cookie', 'cookie_value')
     return response

 # Class-based view
class LandingPageView(TemplateView):
     # Specify the template name
     template_name = 'index.html'

     def get(self, request, *args, **kwargs):
         # Call the superclass's get() method to generate the initial response
         response = super().get(request, *args, **kwargs)

         # Set a cookie named "my_cookie" with a value of "cookie_value"
         response.set_cookie('my_cookie', 'cookie_value')

         return response   
