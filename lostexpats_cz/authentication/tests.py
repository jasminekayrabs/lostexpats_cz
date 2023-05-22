from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.middleware.csrf import get_token



#To run tests, run command "python manage.py test" on terminal
#Test case for XSS protection
class XSSProtectionTestCase(TestCase):
    def test_signup_xss_protection(self):
        # Simulate a POST request with malicious input
        malicious_input = '<script>alert("XSS attack");</script>'
        response = self.client.post(reverse('render_signup'), {
            'fname': malicious_input,
            'lname': malicious_input,
            'email': 'test@example.com',
            'pass1': 'tEst_123',
            'pass2': 'tEst_123',
        })

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Follow the redirect to the login page
        response = self.client.get(response.url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Ensure that the malicious input is properly escaped in the rendered HTML
        self.assertNotContains(response, malicious_input)

        
        

#TEST FOR CSRF PROTECTION
class CSRFProtectionTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('render_signup')
        self.login_url = reverse('render_login')

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
 
