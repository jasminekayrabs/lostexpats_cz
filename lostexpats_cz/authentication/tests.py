from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import escape
import logging
import os
from django.conf import settings



#TEST FOR XSS PROTECTION
class XSSProtectionTestCase(TestCase):
    #SIGNUP
    def test_signup_xss_protection(self):
        # Simulate a POST request with malicious input
        malicious_input = '<script>alert("XSS attack");</script>'
        escaped_input = escape(malicious_input)
        response = self.client.post(reverse('render_signup'), {
            'fname': escaped_input,
            'lname': escaped_input,
            'email': 'test@example.com',
            'pass1': 'tEst_123',
            'pass2': 'tEst_123',
        })

        # Check that the response is a redirect
        # Allow both 301 and 302 redirects
        self.assertIn(response.status_code, (301, 302))  

        # Follow the redirect to the final page
        response = self.client.get(response.url, follow=True)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Ensure that the malicious input is properly escaped in the rendered HTML
        self.assertNotContains(response, malicious_input)
        
    #LOGIN
    def test_login_xss_protection(self):
         # Simulate a POST request with malicious input
        malicious_input = '<script>alert("XSS attack");</script>'
        escaped_input = escape(malicious_input)
        response = self.client.post(reverse('render_login'), {
            'email': escaped_input,
            'pass1': 'tEst_123',
        })
         # Check that the response is a redirect 
         # Allow both 301 and 302 redirects
        self.assertIn(response.status_code, (301, 302)) 

        # Follow the redirect to the final page
        response = self.client.get(response.url, follow=True)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Ensure that the malicious input is properly escaped in the rendered HTML
        self.assertNotContains(response, malicious_input)







#TEST FOR CSRF PROTECTION
class CSRFProtectionTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('render_signup')
        self.login_url = reverse('render_login')

        #SIGNUP
    def test_signup_csrf_protection(self):
        response = self.client.get(self.signup_url, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if CSRF token is present in the response
        self.assertContains(response, 'csrfmiddlewaretoken')  

        # Submit the signup form with CSRF token
        response = self.client.post(
            self.signup_url,
            {'csrfmiddlewaretoken': response.context['csrf_token'], 'fname': 'John', 'lname': 'Doe', 'email': 'john@example.com', 'pass1': 'password', 'pass2': 'password'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)  # Expect a redirect (302) status code

        #LOGIN
    def test_login_csrf_protection(self):
        # Create a user for authentication
        user = User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.get(self.login_url, follow=True)
        self.assertEqual(response.status_code, 200)
         # Check if CSRF token is present in the response
        self.assertContains(response, 'csrfmiddlewaretoken') 

        # Submit the login form with CSRF token
        response = self.client.post(
            self.login_url,
            {'csrfmiddlewaretoken': response.context['csrf_token'], 'email': 'john@example.com', 'pass1': 'password'},
            follow=True
        )
        # Expect a redirect (302) status code
        self.assertEqual(response.status_code, 200)
        
        
#TEST FOR SQL INJECTIONS
class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('render_signup')
        self.login_url = reverse('render_login')
        self.home_url = reverse('home')
        self.user_data = {
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@example.com',
            'pass1': 'password123',
            'pass2': 'password123',
        }

        #SIGNUP
    def test_signup_sql_injection(self):
        # Craft a payload with SQL injection
        payload = {
            'fname': 'John',
            'lname': 'Doe',
            'email': "johndoe@example.com' OR 1=1; --",
            'pass1': 'password123',
            'pass2': 'password123',
        }
        response = self.client.post(self.signup_url, data=payload)
        
        # Verify that the user was not created
        self.assertEqual(response.status_code, 301)
        self.assertFalse(User.objects.filter(email=payload['email']).exists())

        #LOGIN
    def test_login_sql_injection(self):
        # Create a test user
        User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='password123',
        )
        
        # Craft a payload with SQL injection
        payload = {
            'email': "johndoe@example.com' OR 1=1; --",
            'pass1': 'password123',
        }
        response = self.client.post(self.login_url, data=payload)
        
        # Verify that the login failed and user was not authenticated
        self.assertEqual(response.status_code, 301)
        
        #SIGNUP AND LOGIN
    def test_valid_signup_and_login(self):
        # Perform a valid signup
        response = self.client.post(self.signup_url, data=self.user_data)
        
        # Verify that the user was created and redirected to login
        self.assertEqual(response.status_code, 301)
        
        # Perform a valid login
        response = self.client.post(self.login_url, data=self.user_data)
        
        # Verify that the login was successful and user was authenticated
        self.assertEqual(response.status_code, 301)
       
    
# This tests checks to see 1. Existence of the log file:
# 2. Configuration of the logger: It configures the logger named 
# 'user_login' to log messages with the INFO level
# 3.Logging of a test message: It logs the message 'This is a test log message' 
# using the configured logger.
# 4.Presence of the test message in the log file: It reads the contents of the log file specified by log_file_path and checks if the test message ('This is a test log message') is 
# present in the log file using the assertIn assertion.
# Done by Sara 
class LoggingTest(TestCase):
    def test_logging_file(self):
        # Define the log file path
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', '/Users/saraali/Desktop/python_stuff/lostexpats_cz/logs/user_login.log')

        # Ensure the log file exists
        self.assertTrue(os.path.exists('/Users/saraali/Desktop/python_stuff/lostexpats_cz/logs/user_login.log'))

        # Configure the logger
        logger = logging.getLogger('user_login')
        logger.setLevel(logging.INFO)

        # Log a test message
        logger.info('This is a test log message')

        # Read the log file and check if the test message is present
        with open('/Users/saraali/Desktop/python_stuff/lostexpats_cz/logs/user_login.log', 'r') as file:
            log_contents = file.read()
            self.assertIn('This is a test log message', log_contents)

            
# This test checks to see if the is session is secure 
# The purpose of the secure attribute is to prevent cookies
# from being observed by unauthorized parties 
# due to the transmission of the cookie in clear text.
# Done by Sara
class SessionManagementTest(TestCase):
    def test_secure_session(self):
    # Create a client and make a request to a secured view or URL
        response = self.client.get(reverse('secure_view'))

    # Assert that the response status code is as expected
        self.assertEqual(response.status_code, 301)

    # Get the 'sessionid' cookie from the response
        sessionid_cookie = response.cookies.get('sessionid')

        if sessionid_cookie:
        # Assert that the sessionid cookie has the secure flag
           self.assertTrue(sessionid_cookie.get('secure'))

        # Assert that the sessionid cookie has the httponly flag
           self.assertTrue(sessionid_cookie.get('httponly'))
            
            
            
# HSTS test
# 1. It sends a GET request to the 'home' URL with the secure=True parameter, simulating an HTTPS request.
#  This ensures that the request is made over a secure connection.
# 2. It checks if the response status code is 200 (OK) using the assertEqual assertion. 
# This confirms that the URL is accessible and the server responds successfully.
# 3. t checks if the 'Strict-Transport-Security' header is present in the response
# using the assertIn assertion
# 4. It retrieves the value of the 'Strict-Transport-Security' header from the response.
# 5.It checks if the value of the 'Strict-Transport-Security' header matches the expected value using the assertEqual assertion.
# In this case, the expected value is 'max-age=31536000; includeSubDomains', which 
# specifies the HSTS policy's maximum age and includes all subdomains.
# Done by Sara
class HSTSTestCase(TestCase):
    def test_hsts_redirection(self):
        # Send a GET request to the 'home' URL with secure=True to simulate an HTTPS request
        response = self.client.get(reverse('home'), secure=True)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'Strict-Transport-Security' header is present in the response
        self.assertIn('Strict-Transport-Security', response.headers)

        # Retrieve the value of the 'Strict-Transport-Security' header from the response
        hsts_header = response.headers['Strict-Transport-Security']

        # Check if the value of the 'Strict-Transport-Security' header matches the expected value
        self.assertEqual(hsts_header, 'max-age=31536000; includeSubDomains')

    
  
# X frame options 
# pip install requests  
import requests
# Defining the URL to test
url = "http://127.0.0.1:8000/"  
# Sending the HTTP request and retrieving the response headers
try:
    response = requests.get(url)
    x_frame_options = response.headers.get("X-Frame-Options")
# Checking the presence of the "X-Frame-Options" header
    if x_frame_options is None:
        print("X-Frame-Options header is missing")
    else:
        print(f"X-Frame-Options header value: {x_frame_options}")
# Handling exceptions
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
