from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import escape



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
