# REFERRER POLICY BY VERONIKA 

class ReferrerPolicyMiddleware:
# initializes the middleware instance and assigns the get_response parameter to the self.get_response attribute:
    def __init__(self, get_response):
# represents the next middleware in the Django request/response cycle:
        self.get_response = get_response
# accepts the request object as a parameter and is responsible for processing the reques:
    def __call__(self, request):
# passes the request object to the next middleware/view and stores the resulting response in the response variable:
        response = self.get_response(request)
# sets the 'Referrer-Policy' header of the response to the value 'no-referrer':
        response['Referrer-Policy'] = 'no-referrer'
# returns the modified response object with the Referrer policy header set:
        return response


