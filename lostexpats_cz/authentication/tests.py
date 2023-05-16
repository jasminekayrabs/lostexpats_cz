from django.test import TestCase

class XSSProtectionTest(TestCase):
    def test_signup_login_xss_protection(self):
        # Test XSS protection in signup view
        signup_data = {
            'fname': '<script>alert("XSS")</script>',
            'lname': 'Doe',
            'email': 'john@example.com',
            'pass1': 'passW_ord123',
            'pass2': 'passW_ord123',
        }
        response = self.client.post('/render_signup', data=signup_data, follow=True)
        
        # Assert that the response is a successful redirect
        self.assertRedirects(response, '/render_login/')
        
        # Follow the redirect and check the response on the redirected page
        response = self.client.get(response.redirect_chain[0][0])
        
        # Assert that the XSS payload is properly escaped in the response
        self.assertNotContains(response, '<script>')
        
        # Test XSS protection in login view
        login_data = {
            'email': '<script>alert("XSS")</script>',
            'pass1': 'passW_ord123',
        }
        response = self.client.post('/render_login', data=login_data, follow=True)
        
        # Assert that the response is a successful redirect
        self.assertRedirects(response, '/authentication/home/')
        
        # Follow the redirect and check the response on the redirected page
        response = self.client.get(response.redirect_chain[0][0])
        
        # Assert that the XSS payload is properly escaped in the response
        self.assertNotContains(response, '<script>')
