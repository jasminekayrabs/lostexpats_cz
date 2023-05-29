from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.views.generic import TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import logging 
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)




def secure_view(request):
        return render(request, 'secure.html')


@xframe_options_exempt
def ok_to_load_in_a_frame(request):
    return HttpResponse("This page is safe to load in a frame on any site.")

@xframe_options_deny
def view_one(request):
    return HttpResponse("I won't display in any frame!")


@xframe_options_sameorigin
def view_two(request):
    return HttpResponse("Display in a frame if it's from the same origin as me.")



#To store user logs in Log files
logger = logging.getLogger('user_login')


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


def render_index(request):
    return render(request, "authentication/index.html")

#FOR SIGNUP
# By adding csrf_protect here and %csrf_token% in .html files, Django will automatically generate and validate CSRF tokens for each form submission. The CSRF token will be included in the form submission and verified on the server-side, protecting against CSRF attacks.

# By applying the escape function to the user-generated input, you ensure that any HTML tags or special characters are properly escaped and treated as plain text.

@csrf_protect
def render_signup(request):
    if request.method == "POST":
     
        #Retrieve form data
        fname = escape(request.POST['fname'])
        lname = escape(request.POST['lname'])
        email = escape(request.POST['email'])
        password = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        #FOR TERMS AND CONDITIONS
        if not terms_accepted:
            messages.error(request, 'Please accept the Terms and Conditions.')
            return redirect('signup')
     
         #Create user object
        myuser = User.objects.create_user(username=fname, email=email, password=password)
        myuser.email = email
        myuser.first_name = fname
        myuser.last_name = lname 
          #Set user as inactive
        myuser.is_active = False 
        myuser.save()
          
        # Generate activation token
        token = default_token_generator.make_token(myuser)
          
        # Build activation URL
        current_site = get_current_site(request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        activation_url = f"http://{domain}{reverse('activate_account', kwargs={'uidb64': uid, 'token': token})}"
     
        # Render email template with context
        email_context = {
            'user': myuser,
            'activation_url': activation_url,
        }
        email_message = render_to_string('authentication/activation_email.html', email_context)
          
        # Send activation email
        subject = 'Activate your account'
        message = render_to_string('authentication/activation_email.html', {
            'user': myuser,
            'activation_url': activation_url,
        })
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [myuser.email], html_message=email_message)

        return redirect('activation_sent')
    return render(request, "authentication/signup.html")

#RENDER ACTIVATION SENT PAGE
def activation_sent(request):
    return render(request, 'authentication/activation_sent.html')

#Activate account
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('render_login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('home')

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

        else:
            # User authentication failed, display error message
            messages.error(request, "Wrong email or password!")
            return redirect('home')
    
    else:
        email = escape(request.POST.get('email', ''))
        # return render(request, "authentication/login.html")
        form = AuthenticationForm(request)

    # Render the login template with the form,, password reset form, email, and success message
    password_reset_form = PasswordResetView.as_view(
        template_name='authentication/password_reset.html',
        email_template_name='authentication/password_reset_email.html',
        success_url=reverse('password_reset_done')
    )(request=request)

    return render(
        request,
        "authentication/login.html",
        {
            'form': form,
            'password_reset_form': password_reset_form,
            'email': email,
            'success_message': success_message,
        }
    )

# View function for rendering reset password page
class CustomPasswordResetView(PasswordResetView):
    # Specify the template name for the password reset form
    template_name = 'authentication/password_reset.html'
    # Specify the template name for reset password email
    email_template_name = 'authentication/password_reset_email.html'
    # Specify the success url after the password reset is initiated
    success_url = 'reset_password/done/'

# Function for the Reset password done page
class CustomPasswordResetDoneView(PasswordResetDoneView):
    # Specify the template name for reset password done page
    template_name = 'authentication/reset_password_done.html'

# Function for the Reset password confirm page
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # Specify the template name for reset password confirm page
    template_name = 'authentication/password_reset_confirm.html'
    # Specify the success url after the password reset is confirmed
    success_url = 'reset_password/complete/'

# Function for the Reset password complete page
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    # Specify the template name for reset password complete page
    template_name = 'authentication/password_reset_complete.html'
#FOR LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

#Session cookies
def index(request):
     # Create an HTTP response with the message "Welcome to the landing page!"
     response = HttpResponse("Welcome to the landing page!")

     # Set a cookie named "my_cookie" with a value of "cookie_value"
     response.set_cookie('my_cookie', 'cookie_value')
     return response

 # Class-based view
 # For the cookies on the home page
class LandingPageView(TemplateView):
     # Specify the template name
     template_name = 'index.html'

     def get(self, request, *args, **kwargs):
         # Call the superclass's get() method to generate the initial response
         response = super().get(request, *args, **kwargs)

         # Set a cookie named "my_cookie" with a value of "cookie_value"
         response.set_cookie('my_cookie', 'cookie_value')

         return response   
