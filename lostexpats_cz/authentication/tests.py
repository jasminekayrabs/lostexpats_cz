from django.test import TestCase
from django.urls import reverse

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
