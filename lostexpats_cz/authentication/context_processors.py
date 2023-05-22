from django.conf import settings

def cookie_banner(request):
    return {'show_cookie_banner': True}
